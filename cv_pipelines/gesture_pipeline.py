import os
from pathlib import Path
import sys
import cv2
import pandas as pd
import mediapipe as mp

os.environ["CUDA_VISIBLE_DEVICES"] = ""

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import *

from utils.models import *
from utils.geometry import *
from utils.vision import *

# =============================
# LOAD MODELS
# =============================
yolo, yolo_face = load_yolo_models()
hand_landmarker = load_hand_landmarker()
set_yolo(yolo)
set_hand_landmarker(hand_landmarker)

# =============================
# CREATE OUTPUT DIRS
# =============================
os.makedirs(IMAGE_DIRS["gesture"], exist_ok=True)
os.makedirs(os.path.dirname(CSV_PATHS["gesture"]), exist_ok=True)


# =============================
# MAIN PIPELINE
# =============================
def gesture_pipeline(cap):
    face_landmarker = load_face_landmarker()
    records = []
    prev_pitch_yaw = {}
    frame_idx = 0
    row_id = 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    FRAME_STEP = int(fps // 2)
    h, w = None, None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % FRAME_STEP != 0:
            frame_idx += 1
            continue

        if h is None:
            h, w = frame.shape[:2]

        frame_copy = frame.copy()
        yolo_results = yolo(frame)[0]
        students = []

        if len(yolo_results.boxes) > 0:
            xyxy = yolo_results.boxes.xyxy.cpu().numpy()
            cls_ids = yolo_results.boxes.cls.cpu().numpy().astype(int)
            for box, c in zip(xyxy, cls_ids):
                if yolo.names[int(c)] == "student":
                    x1, y1, x2, y2 = box.astype(int)
                    students.append([x1 / w, y1 / h, x2 / w, y2 / h, x1, y1, x2, y2])

        student_records = []
        for sid, student_info in enumerate(students):
            norm_box = student_info[:4]
            px_box = student_info[4:]

            x1, y1, x2, y2 = px_box

            student_crop = frame[y1:y2, x1:x2]
            student_fiddling, student_hand_res = detect_student_hands(student_crop)

            head_action = 0
            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size > 0:
                mp_face = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB),
                )
                face_res_student = face_landmarker.detect(mp_face)
                if (
                    hasattr(face_res_student, "facial_transformation_matrixes")
                    and face_res_student.facial_transformation_matrixes
                ):
                    matrix = face_res_student.facial_transformation_matrixes[0]
                    prev = prev_pitch_yaw.get(sid, (None, None))
                    curr = get_pitch_yaw_from_matrix(matrix)
                    head_action = get_head_nod_shake(prev[0], prev[1], curr[0], curr[1])
                    prev_pitch_yaw[sid] = curr

            jt, it = detect_tools(frame, px_box)
            jt_code = encode_tool(jt)
            it_code = encode_tool(it)
            touching_tool = detect_student_touching_tools(
                frame, px_box, student_hand_res
            )

            color = (
                (0, 0, 255)
                if touching_tool != "-"
                else (0, 165, 255) if jt_code != "-" else (0, 255, 0)
            )
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 3)

            if student_hand_res and student_hand_res.hand_landmarks:
                h_crop, w_crop = student_crop.shape[:2]
                for hand_landmarks in student_hand_res.hand_landmarks:
                    for lm in hand_landmarks:
                        gx = int(lm.x * w_crop) + x1
                        gy = int(lm.y * h_crop) + y1
                        cv2.circle(frame_copy, (gx, gy), 5, (255, 0, 255), -1)

                    for tip_idx in [8, 12]:
                        tip = hand_landmarks[tip_idx]
                        gx = int(tip.x * w_crop) + x1
                        gy = int(tip.y * h_crop) + y1
                        cv2.circle(frame_copy, (gx, gy), 8, (0, 0, 255), -1)

            label_lines = [
                f"S{sid}:H{head_action}F{student_fiddling}T{touching_tool}",
                f"J:{jt_code} I:{it_code}",
            ]
            for i, line in enumerate(label_lines):
                y_pos = y1 - 10 - (i * 25)
                if y_pos > 30:
                    cv2.putText(
                        frame_copy,
                        line,
                        (x1, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )

            student_records.append(
                {
                    "frame": row_id,
                    "student_id": sid,
                    "head_action": head_action,
                    "fiddling": student_fiddling,
                    "joint_tool": jt_code,
                    "individual_tool": it_code,
                    "touching_tool": touching_tool,
                }
            )

            row_id += 1

        global_fiddling, _ = detect_fiddling(frame_copy)
        cv2.putText(
            frame_copy,
            f"GLOBAL H:{global_fiddling}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        out_path = os.path.join(IMAGE_DIRS["gesture"], f"frame_{frame_idx:06d}.jpg")
        cv2.imwrite(out_path, frame_copy)
        records.extend(student_records)
        frame_idx += 1

    cap.release()

    pd.DataFrame(records).to_csv(CSV_PATHS["gesture"], index=False)
    print(" FIXED: Per-student hand detection + per-student face detection!")
    print(f"Processed {len(records)} records")


if __name__ == "__main__":
    gesture_pipeline()
