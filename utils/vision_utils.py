import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
from mediapipe.tasks.python import vision
from deepface import DeepFace

from config import *

mp_face = mp.tasks
BaseOptions = mp_face.BaseOptions
FaceLandmarker = vision.FaceLandmarker
FaceLandmarkerOptions = vision.FaceLandmarkerOptions
VisionRunningMode = vision.RunningMode
Image = mp.Image
ImageFormat = mp.ImageFormat

yolo = None
pose_landmarker = None
hand_landmarker = None
face_landmarker = None


def set_yolo(model):
    global yolo
    yolo = model


def set_pose_landmarker(model):
    global pose_landmarker
    pose_landmarker = model


def set_hand_landmarker(model):
    global hand_landmarker
    hand_landmarker = model


def set_face_landmarker(model):
    global face_landmarker
    face_landmarker = model


def detect_gaze(crop):
    if crop is None or crop.size == 0:
        return np.array([0.2, 0.98])

    crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    mp_img = Image(image_format=ImageFormat.SRGB, data=crop_rgb)
    result = face_landmarker.detect(mp_img)

    if result.face_landmarks and len(result.face_landmarks) > 0:
        lm = result.face_landmarks[0]
        h, w = crop.shape[:2]
        forehead = lm[10]
        chin = lm[152]
        nose = lm[1]

        cx = (forehead.x + chin.x) / 2 * w
        cy = (forehead.y + chin.y) / 2 * h
        nx = nose.x * w
        ny = nose.y * h

        vec = np.array([nx - cx, ny - cy])
        if np.linalg.norm(vec) < 1e-3:
            return np.array([0.2, 0.98])
        return vec / np.linalg.norm(vec) * 100

    return np.array([0.2, 0.98])


def get_gaze_and_head_pose(face_crop):
    if face_crop is None or face_crop.shape[0] == 0 or face_crop.shape[1] == 0:
        return np.array([0.2, 0.98]), None

    crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
    mp_image = Image(image_format=ImageFormat.SRGB, data=crop_rgb)
    result = face_landmarker.detect(mp_image)

    gaze_vec = np.array([0.2, 0.98])
    matrix = None

    if result.face_landmarks and len(result.face_landmarks) > 0:
        lm = result.face_landmarks[0]
        h, w = face_crop.shape[:2]
        forehead = lm[10]
        chin = lm[152]
        center_x = (forehead.x + chin.x) / 2 * w
        center_y = (forehead.y + chin.y) / 2 * h
        nose = lm[1]
        dx = nose.x * w - center_x
        dy = nose.y * h - center_y
        vec = np.array([dx, dy])
        if np.linalg.norm(vec) >= 1e-3:
            gaze_vec = vec / np.linalg.norm(vec) * 100

    if result.facial_transformation_matrixes:
        matrix = result.facial_transformation_matrixes[0]

    return gaze_vec, matrix


def crop_face_from_student(frame, student_box, yolo_face):
    h_img, w_img = frame.shape[:2]
    sx1, sy1, sx2, sy2 = student_box
    sx1 = max(0, min(sx1, w_img))
    sy1 = max(0, min(sy1, h_img))
    sx2 = max(sx1, min(sx2, w_img))
    sy2 = max(sy1, min(sy2, h_img))

    crop = frame[sy1:sy2, sx1:sx2]
    if crop.shape[0] == 0 or crop.shape[1] == 0:
        return crop
    faces = yolo_face(crop)[0]
    if len(faces.boxes) > 0:
        x1, y1, x2, y2 = faces.boxes.xyxy[0].cpu().numpy().astype(int)
        x1 = max(0, min(x1, crop.shape[1]))
        y1 = max(0, min(y1, crop.shape[0]))
        x2 = max(x1, min(x2, crop.shape[1]))
        y2 = max(y1, min(y2, crop.shape[0]))
        face = crop[y1:y2, x1:x2]
        if face.shape[0] > 0 and face.shape[1] > 0:
            return face
    return crop


def safe_crop(frame, x1, y1, x2, y2):
    h, w = frame.shape[:2]
    x1 = max(0, min(x1, w))
    y1 = max(0, min(y1, h))
    x2 = max(0, min(x2, w))
    y2 = max(0, min(y2, h))
    if x2 <= x1 or y2 <= y1:
        return None
    return frame[y1:y2, x1:x2]


def detect_pose(crop):
    if crop is None or crop.size == 0:
        return None
    mp_img = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(crop, cv2.COLOR_BGR2RGB),
    )
    return pose_landmarker.detect(mp_img)


def detect_body_lean(pose_res):
    if not pose_res or not pose_res.pose_landmarks:
        return 0

    lm = pose_res.pose_landmarks[0]

    left = lm[11].x
    right = lm[12].x

    center = (left + right) / 2
    diff = center - 0.5

    if abs(diff) > LEAN_THRESH:
        return 1 if diff > 0 else 2

    return 0


def encode_tool(tool_name):
    """B=block, S=scale, L=laptop, LB=laptop+block, -=none"""
    if not tool_name or tool_name == "":
        return "-"
    tool_name = tool_name.lower()
    if "block" in tool_name:
        return "B"
    elif "scale" in tool_name:
        return "S"
    elif "laptop" in tool_name:
        return "L"
    elif "laptop" in tool_name and "block" in tool_name:
        return "LB"
    return "-"


def detect_student_touching_tools(frame, student_box, hand_res):
    """
    Detect if student hands are touching tools (IoU + Hand fingertip inside tool)
    Returns: 'B'=block, 'S'=scale, 'L'=laptop, '-'=not touching
    """
    if student_box is None or hand_res is None or not hand_res.hand_landmarks:
        return "-"

    student_x1, student_y1, student_x2, student_y2 = student_box
    h_img, w_img = frame.shape[:2]

    results = yolo(frame)[0]
    for det in results.boxes:
        cls = int(det.cls[0])
        tool_label = yolo.names[cls].lower()

        if "student" in tool_label:
            continue

        tx1, ty1, tx2, ty2 = det.xyxy[0].cpu().numpy()

        iou_w = max(0, min(tx2, student_x2) - max(tx1, student_x1))
        iou_h = max(0, min(ty2, student_y2) - max(ty1, student_y1))
        student_area = (student_x2 - student_x1) * (student_y2 - student_y1)
        tool_area = (tx2 - tx1) * (ty2 - ty1)
        iou = (iou_w * iou_h) / (student_area + tool_area + 1e-6)

        if iou > 0.3:
            for hand_landmarks in hand_res.hand_landmarks:
                for tip_idx in [8, 12]:
                    hand_tip = hand_landmarks[tip_idx]
                    hx = int(hand_tip.x * w_img)
                    hy = int(hand_tip.y * h_img)

                    if tx1 <= hx <= tx2 and ty1 <= hy <= ty2:
                        if "block" in tool_label:
                            return "B"
                        elif "scale" in tool_label:
                            return "S"
                        elif "laptop" in tool_label:
                            return "L"

    return "-"


def detect_student_hands(student_crop):
    """Detect hands SPECIFICALLY within student region"""
    if student_crop.size == 0:
        return 0, None

    mp_img = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(student_crop, cv2.COLOR_BGR2RGB),
    )
    hand_res = hand_landmarker.detect(mp_img)
    hands_detected = 1 if hand_res.hand_landmarks else 0
    return hands_detected, hand_res


def detect_fiddling(frame_copy):
    """Detect hands and return hand_res for touching detection + visualization"""
    mp_img = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB),
    )
    hand_res = hand_landmarker.detect(mp_img)

    hands_detected = 1 if hand_res.hand_landmarks else 0

    if hand_res.hand_landmarks:
        h_img, w_img = frame_copy.shape[:2]
        for hand_landmarks in hand_res.hand_landmarks:
            for lm in hand_landmarks:
                x = int(lm.x * w_img)
                y = int(lm.y * h_img)
                cv2.circle(frame_copy, (x, y), 3, (255, 0, 255), -1)
            for tip_idx in [8, 12]:
                tip = hand_landmarks[tip_idx]
                x = int(tip.x * w_img)
                y = int(tip.y * h_img)
                cv2.circle(frame_copy, (x, y), 8, (0, 0, 255), -1)

    return hands_detected, hand_res


def detect_tools(frame, student_box=None):
    joint, individual = "", ""
    results = yolo(frame)[0]

    for det in results.boxes:
        cls = int(det.cls[0])
        label = yolo.names[cls]

        if label not in joint and "student" not in label.lower():
            joint += label + " "

        if student_box is not None:
            x1, y1, x2, y2 = det.xyxy[0].cpu().numpy()
            bx1, by1, bx2, by2 = student_box

            iou_w = max(0, min(x2, bx2) - max(x1, bx1))
            iou_h = max(0, min(y2, by2) - max(y1, by1))
            tool_area = (x2 - x1) * (y2 - y1) + 1e-6

            if (iou_w * iou_h) / tool_area > 0.1 and "student" not in label.lower():
                individual = label
    return joint.strip(), individual


def detect_face_landmarks_task(crop_rgb):
    """Face landmarks using TASKS API (468 points)"""
    try:
        mp_img = Image(image_format=ImageFormat.SRGB, data=crop_rgb)
        results = face_landmarker.detect(mp_img)

        if results.face_landmarks and len(results.face_landmarks) > 0:
            return results.face_landmarks[0]
        return None
    except Exception:
        return None


def detect_emotion(crop_rgb):
    if crop_rgb is None or crop_rgb.size == 0:
        return "neutral"

    try:
        analysis = DeepFace.analyze(
            img_path=crop_rgb,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="retinaface",
            align=True,
        )

        if isinstance(analysis, list) and len(analysis) > 0:
            result = analysis[0]
        else:
            result = analysis

        emotions = result.get("emotion", {})
        if not emotions:
            return "neutral"

        dominant = max(emotions, key=emotions.get)
        confidence = emotions[dominant]
        return dominant.lower() if confidence >= EMOTION_CONF_THRESH else "neutral"

    except Exception:
        return "neutral"


def detect_classroom_emotion(crop_bgr, gaze_vec, lean):
    deepface_emotion = "neutral"

    try:
        crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
        deepface_emotion = detect_emotion(crop_rgb)

        landmarks = detect_face_landmarks_task(crop_rgb)
        if landmarks is None:
            return classify_emotion_simple(deepface_emotion, gaze_vec, lean)

        h, w = crop_rgb.shape[:2]

        def get_point(idx):
            lm = landmarks[idx]
            return (lm.x * w, lm.y * h)

        mouth_left = get_point(61)
        mouth_right = get_point(291)
        mouth_top = get_point(13)
        mouth_bottom = get_point(14)
        forehead = get_point(10)
        nose = get_point(1)

        mouth_width = abs(mouth_right[0] - mouth_left[0])
        mouth_height = abs(mouth_bottom[1] - mouth_top[1])
        smile_ratio = mouth_height / max(mouth_width, 1)
        mouth_openness = mouth_height / h
        head_tilt_back = forehead[1] < nose[1] * 0.9

        if smile_ratio < 0.28 and mouth_openness > 0.08:
            return "positive"

        if smile_ratio < 0.30 and head_tilt_back:
            return "positive"

        if deepface_emotion == "happy":
            return "positive"

    except Exception:
        pass

    return classify_emotion_simple(deepface_emotion, gaze_vec, lean)


def classify_emotion_simple(deepface_emotion, gaze_vec, lean):
    if deepface_emotion in ["happy"]:
        return "positive"
    if deepface_emotion in ["sad", "angry", "fear", "disgust"]:
        return "negative"

    gaze_mag = np.linalg.norm(gaze_vec)
    if gaze_mag > 50 or lean != 0:
        return "bored"

    return "confusion"


def temporal_smoothing(student_emotions, emotion, sid):
    if sid not in student_emotions:
        student_emotions[sid] = []

    student_emotions[sid].append(emotion)
    if len(student_emotions[sid]) > 10:
        student_emotions[sid].pop(0)

    recent = student_emotions[sid][-3:]
    if emotion == "positive" and any(e == "positive" for e in recent):
        return "positive"
    return emotion
