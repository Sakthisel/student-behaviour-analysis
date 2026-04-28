import os
from pathlib import Path
import sys
import numpy as np
import pandas as pd

os.environ["CUDA_VISIBLE_DEVICES"] = ""

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import *

from utils.model_utils import *
from utils.geometry import *
from utils.vision_utils import *
from utils.drawing import *

# =============================
# LOAD MODELS
# =============================
yolo, yolo_face = load_yolo_models()
face_landmarker = load_face_landmarker()
set_face_landmarker(face_landmarker)

# =============================
# CREATE OUTPUT DIRS
# =============================
os.makedirs(IMAGE_DIRS["gaze"], exist_ok=True)
os.makedirs(os.path.dirname(CSV_PATHS["gaze"]), exist_ok=True)


# =============================
# MAIN PIPELINE
# =============================
def gaze_pipeline(cap):
    records = []
    frame_idx = FRAME_INDEX
    row_id = 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    FRAME_STEP = max(1, int(fps // 2))
    trackid_to_sid = {}
    next_sid = 0
    last_seen = {}
    student_head_pose = {}

    print("Processing video with TRACKING + gaze + stable IDs...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % FRAME_STEP != 0:
            frame_idx += 1
            continue

        results = yolo.track(frame, persist=True, tracker="bytetrack.yaml")[0]
        students, all_objects = [], []

        if results.boxes is not None and len(results.boxes) > 0:

            xyxy = results.boxes.xyxy.cpu().numpy()
            cls_id = results.boxes.cls.cpu().numpy().astype(int)
            confs = results.boxes.conf.cpu().numpy()

            track_ids = (
                results.boxes.id.cpu().numpy().astype(int)
                if results.boxes.id is not None
                else [-1] * len(xyxy)
            )

            for box, c, conf, tid in zip(xyxy, cls_id, confs, track_ids):
                if conf < 0.4:
                    continue

                x1, y1, x2, y2 = box.astype(int)
                cls_name = results.names[int(c)]

                if cls_name in ["person", "student"]:
                    students.append((x1, y1, x2, y2, float(conf), tid))
                else:
                    all_objects.append((x1, y1, x2, y2, cls_name, float(conf)))

        frame_copy = frame.copy()
        active_track_ids = set()

        for sx1, sy1, sx2, sy2, sconf, track_id in students:

            if track_id == -1:
                continue

            active_track_ids.add(track_id)

            if track_id not in trackid_to_sid:
                trackid_to_sid[track_id] = next_sid
                next_sid += 1

            s_id = trackid_to_sid[track_id]
            last_seen[track_id] = frame_idx

            face_crop = crop_face_from_student(frame, (sx1, sy1, sx2, sy2), yolo_face)
            if face_crop is None:
                continue

            gaze_vec, head_matrix = get_gaze_and_head_pose(face_crop)

            if gaze_vec is None:
                continue

            norm = np.linalg.norm(gaze_vec)
            if norm < 1e-6:
                continue

            gaze_vec = gaze_vec / norm
            face_x = (sx1 + sx2) // 2
            face_y = sy1 + int(0.25 * (sy2 - sy1))
            looking_at = "none"
            looking_other_student = 0

            draw_gaze_cone(
                frame_copy,
                (face_x, face_y),
                gaze_vec,
                angle_deg=ANGLE_THRESH,
                length=DIST_THRESH,
            )

            best_obj = None
            best_dist = float("inf")

            for ox1, oy1, ox2, oy2, obj_name, oconf in all_objects:

                if oconf < MIN_CONFIDENCE:
                    continue

                if is_occluded((ox1, oy1, ox2, oy2), (sx1, sy1, sx2, sy2)):
                    continue

                cx, cy = box_center(ox1, oy1, ox2, oy2)
                vec = np.array([cx - face_x, cy - face_y])
                dist = np.linalg.norm(vec)

                if dist < 1e-6:
                    continue

                ang = angle_between(gaze_vec, vec)

                if dist <= DIST_THRESH and ang <= ANGLE_THRESH:
                    if dist < best_dist:
                        best_dist = dist
                        best_obj = (ox1, oy1, ox2, oy2, obj_name, cx, cy)

            if best_obj:
                ox1, oy1, ox2, oy2, obj_name, cx, cy = best_obj
                looking_at = obj_name

                cv2.rectangle(frame_copy, (ox1, oy1), (ox2, oy2), (0, 0, 255), 3)
                cv2.line(
                    frame_copy,
                    (face_x, face_y),
                    (int(cx), int(cy)),
                    (255, 255, 0),
                    2,
                )

            for ox1, oy1, ox2, oy2, _, other_tid in students:
                if other_tid == track_id:
                    continue

                cx, cy = box_center(ox1, oy1, ox2, oy2)
                vec = np.array([cx - face_x, cy - face_y])
                dist = np.linalg.norm(vec)

                if dist < 1e-6:
                    continue

                ang = angle_between(gaze_vec, vec)

                if dist <= DIST_THRESH and ang <= ANGLE_THRESH:
                    looking_other_student = 1

                    cv2.arrowedLine(
                        frame_copy,
                        (face_x, face_y),
                        (int(cx), int(cy)),
                        (255, 0, 0),
                        3,
                        tipLength=0.2,
                    )
                    break

            prev_pitch, prev_yaw = student_head_pose.get(s_id, (None, None))
            head_nod_shake = 0

            if head_matrix is not None:
                curr_pitch, curr_yaw = get_pitch_yaw_from_matrix(head_matrix)

                head_nod_shake = get_head_nod_shake(
                    prev_pitch, prev_yaw, curr_pitch, curr_yaw
                )

                student_head_pose[s_id] = (curr_pitch, curr_yaw)

            color = (0, 255, 0) if looking_at != "none" else (0, 255, 255)

            cv2.rectangle(frame_copy, (sx1, sy1), (sx2, sy2), color, 2)
            draw_text(frame_copy, f"TID:{track_id}", (sx1, sy1 - 45), (255, 255, 0))

            gaze_end_x = face_x + int(gaze_vec[0] * 100)
            gaze_end_y = face_y + int(gaze_vec[1] * 100)

            cv2.line(
                frame_copy,
                (face_x, face_y),
                (gaze_end_x, gaze_end_y),
                (0, 255, 255),
                3,
            )

            draw_text(frame_copy, f"Looking: {looking_at}", (sx1, sy2 + 15))
            draw_text(frame_copy, f"Head: {head_nod_shake}", (sx1, sy2 + 35))

            records.append(
                {
                    "frame": row_id,
                    "student_id": s_id,
                    "joint_visual_attention": (
                        "L"
                        if looking_at == "laptop"
                        else "B" if looking_at == "block" else "N"
                    ),
                    "individual_attention": 1 if looking_at == "scale" else 0,
                    "looking_other_student": looking_other_student,
                    "looking_away": (
                        1
                        if looking_at not in ["scale", "block", "laptop", "student"]
                        else 0
                    ),
                    "head_nod_shake": head_nod_shake,
                    "confidence": round(float(sconf), 2),
                }
            )

            row_id += 1 

        to_delete = []
        for tid, last in last_seen.items():
            if frame_idx - last > MAX_MISSING:
                to_delete.append(tid)

        for tid in to_delete:
            last_seen.pop(tid, None)

        out_path = os.path.join(IMAGE_DIRS["gaze"], f"frame_{frame_idx:06d}.jpg")
        cv2.imwrite(out_path, frame_copy)

        frame_idx += 1

    cap.release()

    pd.DataFrame(records).to_csv(CSV_PATHS["gaze"], index=False)

    print(" FINAL pipeline complete!")
    print(f"Processed {len(records)} records")


if __name__ == "__main__":
    gaze_pipeline()
