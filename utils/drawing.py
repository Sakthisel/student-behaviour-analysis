import cv2
import numpy as np
from config import *


def draw_text(img, text, pos, color=(255, 255, 255)):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)


def draw_gaze_cone(
    img, start, vec, angle_deg=ANGLE_THRESH, length=DIST_THRESH, color=(0, 255, 0)
):
    if np.linalg.norm(vec) < 1e-3:
        return
    vx, vy = vec / np.linalg.norm(vec) * length
    main_end = (int(start[0] + vx), int(start[1] + vy))
    cv2.line(img, start, main_end, color, 2)
    angle_rad = np.radians(angle_deg)
    rot_matrix1 = np.array(
        [
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad), np.cos(angle_rad)],
        ]
    )
    rot_matrix2 = np.array(
        [
            [np.cos(-angle_rad), -np.sin(-angle_rad)],
            [np.sin(-angle_rad), np.cos(-angle_rad)],
        ]
    )
    edge1 = rot_matrix1 @ np.array([vx, vy])
    edge2 = rot_matrix2 @ np.array([vx, vy])
    cv2.line(img, start, (int(start[0] + edge1[0]), int(start[1] + edge1[1])), color, 1)
    cv2.line(img, start, (int(start[0] + edge2[0]), int(start[1] + edge2[1])), color, 1)


def draw_pose(frame, pose_res, x1, y1, crop_shape):
    if not pose_res or not pose_res.pose_landmarks:
        return
    h, w = crop_shape[:2]
    for lm in pose_res.pose_landmarks[0]:
        x = int(lm.x * w) + x1
        y = int(lm.y * h) + y1
        cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)
