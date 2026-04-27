import cv2
import os
import numpy as np
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import VIDEO_PATH

BASE_DIR = Path(__file__).resolve().parent.parent

output_dir = "dataset/frames"

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(BASE_DIR / VIDEO_PATH)

if not cap.isOpened():
    print(f"Error: Unable to open video file {VIDEO_PATH}")
    exit()

frame_id = 0
saved_id = 0
skip = 30
target_width = 640
target_height = 480

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # ============================================
    # Save the frame every 'skip' frames
    # # ============================================
    if frame_id % skip == 0:
        frame_filename = f"{output_dir}/frame_{saved_id:05d}.jpg"
        cv2.imwrite(frame_filename, frame)
        saved_id += 1

    frame_id += 1

# ============================================
# Release the video capture object
# ============================================
cap.release()

# ============================================
# Print how many frames were saved
# ============================================
print(f"Saved {saved_id} frames.")
