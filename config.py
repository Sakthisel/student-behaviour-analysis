import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =============================
# CONSTANTS
# =============================
FRAME_INDEX = 0
FRAME_STEP = 15
MAX_MISSING = 30

PITCH_THRESH = 15
YAW_THRESH = 10
LEAN_THRESH = 0.15

MIN_OBJ_AREA = 1000
MAX_OBJ_AREA = 140000
MIN_CONFIDENCE = 0.25

ANGLE_THRESH = 65
DIST_THRESH = 1000

IOU_THRESH = 0.3
MAX_MISSED = 10

EMOTION_CONF_THRESH = 30.0

# =============================
# MODELS
# =============================
FACE_MODEL_PATH = "models/mediapipe_models/face_landmarker.task"
POSE_MODEL_PATH = "models/mediapipe_models/pose_landmarker_lite.task"
HAND_MODEL_PATH = "models/mediapipe_models/hand_landmarker.task"

YOLO_V8_MODEL = "models/yolo_models/yolov8n.pt"
YOLO_MODEL_PATH = "custom_yolo/runs/trained_model/weights/best.pt"
YOLO_FACE_MODEL_PATH = "models/yolo_models/yolov8n-face.pt"

# =============================
# INPUT PATH
# =============================
VIDEO_PATH = "videos/classroom_sample.mov"

# =============================
# TRAINED MODEL
# =============================
BEHAVIOUR_MODEL = "models/ml_trained_models/behavior_model.pkl"

# =============================
# CV PIPELINES PATHS
# =============================
OUTPUT_BASE = "outputs"

CSV_PATHS = {
    "gaze": f"{OUTPUT_BASE}/csv/gaze.csv",
    "gesture": f"{OUTPUT_BASE}/csv/gesture.csv",
    "pose": f"{OUTPUT_BASE}/csv/pose.csv",
    "emotion": f"{OUTPUT_BASE}/csv/emotion.csv",
    "final": f"{OUTPUT_BASE}/csv/final_combined.csv",
    "merged": f"{OUTPUT_BASE}/csv/merged.csv",
    "summary": f"{OUTPUT_BASE}/csv/student_summary.csv",
}

IMAGE_DIRS = {
    "gaze": f"{OUTPUT_BASE}/images/gaze",
    "gesture": f"{OUTPUT_BASE}/images/gesture",
    "pose": f"{OUTPUT_BASE}/images/pose",
    "emotion": f"{OUTPUT_BASE}/images/emotion",
    "merged": f"{OUTPUT_BASE}/images/merged",
}
