import numpy as np
from config import *


def box_center(x1, y1, x2, y2):
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def angle_between(v1, v2):
    v1, v2 = np.array(v1, float), np.array(v2, float)
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 < 1e-6 or n2 < 1e-6:
        return 180.0
    cosang = np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0)
    return np.degrees(np.arccos(cosang))


def get_pitch_yaw_from_matrix(matrix):
    r = np.array(matrix).reshape(4, 4)[:3, :3]
    pitch = np.arctan2(-r[2, 1], r[2, 2])
    yaw = np.arctan2(r[2, 0], np.sqrt(r[2, 1] ** 2 + r[2, 2] ** 2))
    return np.degrees(pitch), np.degrees(yaw)


def get_head_nod_shake(prev_pitch, prev_yaw, curr_pitch, curr_yaw):
    if prev_pitch is None or prev_yaw is None:
        return 0
    pitch_diff = curr_pitch - prev_pitch
    yaw_diff = curr_yaw - prev_yaw
    if (abs(pitch_diff) > PITCH_THRESH and abs(yaw_diff) < YAW_THRESH) or (
        abs(yaw_diff) > YAW_THRESH and abs(pitch_diff) < PITCH_THRESH
    ):
        return 1
    return 0


def is_occluded(obj_box, student_box, overlap_thresh=0.4):
    ox1, oy1, ox2, oy2 = obj_box
    sx1, sy1, sx2, sy2 = student_box
    x1 = max(ox1, sx1)
    y1 = max(oy1, sy1)
    x2 = min(ox2, sx2)
    y2 = min(oy2, sy2)
    if x2 <= x1 or y2 <= y1:
        return False
    intersect_area = (x2 - x1) * (y2 - y1)
    obj_area = (ox2 - ox1) * (oy2 - oy1)
    return (intersect_area / obj_area) > overlap_thresh


def iou(a, b):
    xA = max(a[0], b[0])
    yA = max(a[1], b[1])
    xB = min(a[2], b[2])
    yB = min(a[3], b[3])
    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = (a[2] - a[0]) * (a[3] - a[1])
    areaB = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (areaA + areaB - inter + 1e-6)
