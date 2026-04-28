# ⚙️ Setup Guide

## Requirements

- Python 3.9+
- pip
- (Optional) GPU for faster processing

## Setup

Run:

`sh scripts/setup.sh`

This will:
- Install dependencies
- Prepare environment

## Run Project

`sh scripts/run.sh`

## Input

Place videos in:
videos/

Supported formats:
- .mp4
- .avi

## Output

`outputs/csv/student_summary.csv`
`models/ml_trained_models/`

## Notes

- Ensure video path is correct in config.py
- Make scripts executable if needed:

`chmod +x setup.sh run.sh`