# Computer Vision Pipeline (cv_pipelines)

This section explains how video data is processed using Computer Vision techniques to extract student behavioral features such as gaze, gesture, pose, and emotion.

---

## Input Data

The pipeline takes video input of group discussions.

Example:
input_videos/discussion.mp4

---

## Pipeline Overview

The CV pipeline performs the following steps:

1. Convert video into frames  
2. Detect students using YOLO  
3. Track multiple participants  
4. Extract behavioral features  
5. Store results in CSV files  
6. Aggregate data into final summary  

---

## Step 1: Video to Frames

The input video is split into individual frames for processing.

- Each frame is processed independently  
- Frame rate is configurable  

---

## Step 2: Student Detection (YOLO)

YOLO model is used to detect students in each frame.

- Detect multiple people  
- Draw bounding boxes  
- Assign unique IDs  

Model used:
runs/trained_models/weights/best.pt

---

## Step 3: Multi-Object Tracking

Each detected student is tracked across frames.

- Assign unique ID per student  
- Maintain consistency across frames  

---

## Step 4: Gaze Detection

Analyzes where the student is looking.

- Forward gaze → attentive  
- Away gaze → less attentive  

---

## Step 5: Gesture Detection

Detects hand and body movements.

- Active gestures → high engagement  
- Passive behavior → low engagement  

---

## Step 6: Pose Estimation

Tracks body posture using keypoints.

- Upright posture → attentive  
- Slouching → low attention  

---

## Step 7: Emotion Detection

Detects facial expressions.

- Happy / Interested → engaged  
- Neutral / Sad → less engaged  

---

## Step 8: CSV Generation

For each frame and student, data is stored in CSV format.

Example:
outputs/csv/frame_data.csv

Columns include:
- student_id  
- gaze_score  
- gesture_score  
- pose_score  
- emotion_score  

---

## Step 9: Aggregation

All frame-level data is aggregated into final student summary.

Output:
outputs/csv/student_summary.csv

Example:

student_id,attention_score,engagement_score,gd_score  
0,2.42,1.90,4.33  
1,2.04,1.74,3.78  

---

## Run CV Pipeline

Run the complete pipeline:

python -m cv_pipelines.main

---

## Output Files

- Frame-level CSVs  
- Aggregated student_summary.csv  

---

## Key Notes

- Ensure video quality is clear  
- Lighting affects detection accuracy  
- Multiple participants must be visible  
- YOLO model must be trained before running  

---

## Recommendation

- Use high-resolution videos  
- Keep camera stable  
- Ensure clear face visibility  
- Combine CV output with ML + LLM for best results  

---

## Summary

The CV pipeline converts raw video into structured behavioral data, which is then used by ML models for prediction and LLMs for report generation.