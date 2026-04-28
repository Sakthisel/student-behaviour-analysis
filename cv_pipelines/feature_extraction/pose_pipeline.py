from pathlib import Path
import sys
import cv2
import os
import pandas as pd

os.environ["CUDA_VISIBLE_DEVICES"] = ""

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import *

from utils.model_utils import *
from utils.drawing import draw_pose
from utils.geometry import iou
from utils.vision_utils import *


# =============================
# LOAD MODELS
# =============================
yolo_model, _ = load_yolo_models()
pose_landmarker = load_pose_landmarker()
set_pose_landmarker(pose_landmarker)

# =============================
# CREATE OUTPUT DIRS
# =============================
os.makedirs(IMAGE_DIRS["pose"], exist_ok=True)
os.makedirs(os.path.dirname(CSV_PATHS["pose"]), exist_ok=True)


# =============================
# MAIN PIPELINE
# =============================
def pose_pipeline(cap):
    frame_idx = 0
    row_id = 1
    records = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    FRAME_STEP = int(fps // 2)
    tracks = {}
    missed = {}
    lean_time = {}
    next_id = 0
    MAX_MISSED = 10

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % FRAME_STEP != 0:
            frame_idx += 1
            continue

        frame_copy = frame.copy()
        detections = []

        yolo_res = yolo_model(frame)[0]

        if yolo_res.boxes is not None:
            for box, cls in zip(yolo_res.boxes.xyxy, yolo_res.boxes.cls):
                box = box.cpu().numpy()
                cls = int(cls)
                if yolo_model.names[cls].lower() == "student":
                    detections.append(box.astype(int))

        updated_tracks = {}
        used_ids = set()

        for det in detections:
            best_iou, best_id = 0, None
            for tid, prev in tracks.items():
                score = iou(det, prev)
                if score > best_iou:
                    best_iou, best_id = score, tid

            if best_iou > IOU_THRESH and best_id not in used_ids:
                updated_tracks[best_id] = det
                missed[best_id] = 0
                used_ids.add(best_id)
            else:
                updated_tracks[next_id] = det
                missed[next_id] = 0
                lean_time[next_id] = 0.0
                next_id += 1

        for tid in tracks:
            if tid not in updated_tracks:
                missed[tid] += 1
                if missed[tid] < MAX_MISSED:
                    updated_tracks[tid] = tracks[tid]

        tracks = updated_tracks

        for sid, (x1, y1, x2, y2) in tracks.items():
            crop = safe_crop(frame, x1, y1, x2, y2)
            pose_res = detect_pose(crop)
            lean = detect_body_lean(pose_res)

            if lean != 0:
                lean_time[sid] += 1 / fps

            if crop is not None:
                draw_pose(frame_copy, pose_res, x1, y1, crop.shape)

            color = (
                (0, 255, 0)
                if lean == 0
                else (0, 165, 255) if lean == 1 else (0, 0, 255)
            )

            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame_copy,
                f"ID:{sid} L:{lean}",
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

            records.append(
                {
                    "frame": row_id,
                    "student_id": sid,
                    "lean": lean,
                    "lean_seconds": round(lean_time.get(sid, 0), 2),
                    "lean_towards": 1 if lean == 1 else 0,
                    "lean_away": 1 if lean == 2 else 0,
                }
            )

            row_id += 1

        out_path = os.path.join(IMAGE_DIRS["pose"], f"frame_{frame_idx:06d}.jpg")
        cv2.imwrite(out_path, frame_copy)
        frame_idx += 1

    cap.release()

    pd.DataFrame(records).to_csv(CSV_PATHS["pose"], index=False)
    print(" FIXED: Per-student pose detection!")
    print(f"Processed {len(records)} records")


if __name__ == "__main__":
    pose_pipeline()
