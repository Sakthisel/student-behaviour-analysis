# 🚀 Pipeline Documentation

## Overview

This system processes group discussion videos and analyzes student behavior using Computer Vision, Machine Learning, and LLM.

## Pipeline Flow

Video Input
→ YOLO Detection & Tracking
→ Feature Extraction (Gaze, Gesture, Pose, Emotion)
→ CSV Generation
→ Data Aggregation & GD Score
→ ML Models + LSTM
→ Engagement Prediction
→ LLM Report Generation

## Modules

1. YOLO (custom_yolo)
- Detects multiple students
- Assigns tracking IDs
- Output: bounding boxes

2. CV Pipeline (cv_pipelines)
Extracts:
- Gaze → Attention
- Gesture → Activity
- Pose → Posture
- Emotion → Expression

Output:
outputs/csv/student_summary.csv

3. ML Pipeline (ml)

Models:
- Random Forest
- SVM
- XGBoost
- LightGBM
- LSTM

Output:
models/trained_models/

4. LLM (llm)
- Converts predictions into reports
- Uses Gemini or fine-tuned model

## Final Output

- CSV Summary
- ML Predictions
- LLM Reports

## Run Pipeline

python -m main