import os
from pathlib import Path
import sys
import pandas as pd
from collections import defaultdict

os.environ["CUDA_VISIBLE_DEVICES"] = ""

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import *

from utils.model_utils import *
from utils.geometry import box_center
from utils.vision_utils import *

# =============================
# LOAD MODELS
# =============================
yolo, yolo_face = load_yolo_models()
face_landmarker = load_face_landmarker()
pose_landmarker = load_pose_landmarker()
set_face_landmarker(face_landmarker)
set_pose_landmarker(pose_landmarker)


# =============================
# CREATE OUTPUT DIRS
# =============================
os.makedirs(IMAGE_DIRS["emotion"], exist_ok=True)
os.makedirs(os.path.dirname(CSV_PATHS["emotion"]), exist_ok=True)


def emotion_pipeline(cap):
    frame_idx = 0
    row_id = 1
    records = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    FRAME_STEP = max(1, int(fps // 2))

    student_emotions = defaultdict(list)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_frame = frame_idx
        frame_idx += 1

        if current_frame % FRAME_STEP != 0:
            continue

        frame_copy = frame.copy()
        detections = []

        yolo_res = yolo(frame)[0]
        boxes_xyxy = yolo_res.boxes.xyxy.cpu().numpy()
        classes = yolo_res.boxes.cls.cpu().numpy().astype(int)

        for box, cls in zip(boxes_xyxy, classes):
            if yolo.names[cls].lower() == "student":
                detections.append(box.astype(int))

        for sid, (x1, y1, x2, y2) in enumerate(detections):
            h_img, w_img = frame.shape[:2]
            x1_cl = max(0, min(x1, w_img))
            y1_cl = max(0, min(y1, h_img))
            x2_cl = max(x1_cl, min(x2, w_img))
            y2_cl = max(y1_cl, min(y2, h_img))

            if x2_cl <= x1_cl or y2_cl <= y1_cl:
                continue

            full_crop = frame[y1_cl:y2_cl, x1_cl:x2_cl]
            h_box = y2_cl - y1_cl
            face_y2 = y1_cl + int(0.75 * h_box)
            face_crop = frame[y1_cl:face_y2, x1_cl:x2_cl]

            gaze_vec = detect_gaze(full_crop)
            pose_res = detect_pose(full_crop)
            lean = detect_body_lean(pose_res)
            emotion = detect_classroom_emotion(face_crop, gaze_vec, lean)
            emotion = temporal_smoothing(student_emotions, emotion, sid)

            face_cx, face_cy = box_center(x1_cl, y1_cl, x2_cl, y2_cl)
            end_x = int(face_cx + gaze_vec[0])
            end_y = int(face_cy + gaze_vec[1])

            cv2.rectangle(frame_copy, (x1_cl, y1_cl), (x2_cl, y2_cl), (0, 255, 0), 2)
            cv2.line(
                frame_copy,
                (int(face_cx), int(face_cy)),
                (end_x, end_y),
                (0, 255, 255),
                2,
            )

            color = {
                "positive": (0, 255, 255),
                "negative": (0, 0, 255),
                "bored": (128, 128, 128),
                "confusion": (255, 0, 255),
            }.get(emotion, (0, 0, 255))

            label = f"ID:{sid} L:{lean} {emotion}"

            cv2.putText(
                frame_copy,
                label,
                (x1_cl, y1_cl - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

            emotion_binary = {
                "positive": 1 if emotion == "positive" else 0,
                "negative": 1 if emotion == "negative" else 0,
                "bored": 1 if emotion == "bored" else 0,
                "confusion": 1 if emotion == "confusion" else 0,
            }

            records.append(
                {
                    "frame": row_id,
                    "student_id": sid,
                    "positive": emotion_binary["positive"],
                    "negative": emotion_binary["negative"],
                    "bored": emotion_binary["bored"],
                    "confusion": emotion_binary["confusion"],
                }
            )

            row_id += 1

        out_path = os.path.join(IMAGE_DIRS["emotion"], f"frame_{current_frame:06d}.jpg")
        cv2.imwrite(out_path, frame_copy)

    cap.release()

    pd.DataFrame(records).to_csv(CSV_PATHS["emotion"], index=False)
    print(" Emotion pipeline complete!")
    print(f"Processed {len(records)} records")


if __name__ == "__main__":
    emotion_pipeline()
