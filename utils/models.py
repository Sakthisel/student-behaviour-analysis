import mediapipe as mp
from mediapipe.tasks.python import vision
from ultralytics import YOLO
from config import *


BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = vision.RunningMode


def load_yolo_models():
    yolo = YOLO(YOLO_MODEL_PATH)
    yolo_face = YOLO(YOLO_FACE_MODEL_PATH)
    return yolo, yolo_face


def load_face_landmarker():
    FaceLandmarker = vision.FaceLandmarker
    FaceLandmarkerOptions = vision.FaceLandmarkerOptions

    face_options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=FACE_MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_faces=1,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=True,
    )

    return FaceLandmarker.create_from_options(face_options)


def load_hand_landmarker():
    HandLandmarker = vision.HandLandmarker
    HandLandmarkerOptions = vision.HandLandmarkerOptions

    hand_options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=HAND_MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=2,
    )

    return HandLandmarker.create_from_options(hand_options)


def load_pose_landmarker():
    PoseLandmarker = vision.PoseLandmarker
    PoseLandmarkerOptions = vision.PoseLandmarkerOptions

    pose_options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=POSE_MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_poses=1,
    )

    return PoseLandmarker.create_from_options(pose_options)
