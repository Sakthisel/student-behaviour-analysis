import os
import sys
import subprocess
from pathlib import Path

import pandas as pd

from app.core.config import PROJECT_ROOT, STUDENT_SUMMARY_PATH

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from llm.inference.gemini import generate_report


def run_analysis_pipeline(video_path: Path):
    env = os.environ.copy()
    env["VIDEO_PATH"] = str(video_path)

    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("VIDEO_PATH:", video_path)

    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
    )

    print("PIPELINE STDOUT:")
    print(result.stdout)

    print("PIPELINE STDERR:")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(result.stderr or "Pipeline failed")

    return build_response_from_csv()


def build_response_from_csv():
    if not STUDENT_SUMMARY_PATH.exists():
        raise FileNotFoundError(f"Missing file: {STUDENT_SUMMARY_PATH}")

    df = pd.read_csv(STUDENT_SUMMARY_PATH)

    # Ensure column exists
    if "ml_engagement" not in df.columns:
        df["ml_engagement"] = "LOW"

    # Convert to frontend format
    students = [
        {
            "student_id": int(row["student_id"]),
            "attention_score": round(float(row["attention_score"]), 2),
            "engagement_score": round(float(row["engagement_score"]), 2),
            "gd_score": round(float(row["gd_score"]), 2),
            "ml_engagement": str(row["ml_engagement"]).upper(),
        }
        for _, row in df.iterrows()
    ]

    trend_data = [
        {
            "frame": i + 1,
            "attention": s["attention_score"],
            "engagement": s["engagement_score"],
            "gd": s["gd_score"],
        }
        for i, s in enumerate(students)
    ]

    try:
        report = generate_report(students)
    except:
        report = "Report generation failed."

    return {
        "students": students,
        "trendData": trend_data,
        "report": report,
    }
