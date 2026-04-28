from pathlib import Path
import sys

# ==========================
# IMPORT CONFIG
# ==========================
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import *

# ==========================
# PATH SETUP
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

from custom_yolo.inference.yolo_predict import run_inference
from custom_yolo.training.yolo_train import train_model

VIDEO_PATH = BASE_DIR / "videos/classroom_sample.mov"
YOLO_OBJECT_PATH = BASE_DIR / "custom_yolo/config/objects.yaml"
OUTPUT_PATH = BASE_DIR / "custom_yolo"

YOLO_V8_MODEL_PATH = Path(YOLO_V8_MODEL or "models/yolo_models/yolov8n.pt")


# ==========================
# CHECK FILES
# ==========================
def check_files():
    print("\nChecking files...")

    print("Video:", VIDEO_PATH)
    print("Dataset:", YOLO_OBJECT_PATH)

    if not VIDEO_PATH.exists():
        raise FileNotFoundError(f"Video not found: {VIDEO_PATH}")

    if not YOLO_OBJECT_PATH.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {YOLO_OBJECT_PATH}")

    print("All files found!\n")


# ==========================
# MAIN PIPELINE
# ==========================
if __name__ == "__main__":
    check_files()

    # STEP 1: Train
    model = train_model(YOLO_V8_MODEL_PATH, YOLO_OBJECT_PATH, OUTPUT_PATH)

    # STEP 2: Inference using trained model
    run_inference(VIDEO_PATH, model, OUTPUT_PATH)
