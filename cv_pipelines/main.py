from multiprocessing import Process, set_start_method
from pathlib import Path
import sys
import time
import cv2
import traceback

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import VIDEO_PATH

from cv_pipelines.feature_extraction.gaze_pipeline import gaze_pipeline
from cv_pipelines.feature_extraction.gesture_pipeline import gesture_pipeline
from cv_pipelines.feature_extraction.pose_pipeline import pose_pipeline
from cv_pipelines.feature_extraction.emotion_pipeline import emotion_pipeline

from cv_pipelines.processing.combine_pipeline import combine
from cv_pipelines.processing.gd_scoring import compute_scores


# =============================
# SAFE RUN WRAPPER
# =============================
def run_safe(fn, name, video_path):
    print(f"Starting {name}...", flush=True)

    cap = None

    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fn(cap)

        print(f"Finished {name}", flush=True)

    except Exception as e:
        print(f"{name} error: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    finally:
        if cap is not None:
            cap.release()


# =============================
# MAIN
# =============================
def cv_pipelines():
    try:
        set_start_method("spawn", force=True)
    except RuntimeError:
        pass

    start_time = time.time()

    video_path = str(VIDEO_PATH)

    pipeline_jobs = [
        ("gaze", gaze_pipeline),
        ("gesture", gesture_pipeline),
        ("pose", pose_pipeline),
    ]

    processes = []
    failed = []

    # =============================
    # RUN PARALLEL PIPELINES
    # =============================
    for name, fn in pipeline_jobs:
        p = Process(
            target=run_safe,
            args=(fn, name, video_path),
            name=name,
        )
        processes.append((name, p))
        p.start()

    for name, p in processes:
        p.join()

        if p.exitcode != 0:
            failed.append((name, p.exitcode))

    # =============================
    # EMOTION PIPELINE
    # =============================
    run_safe(emotion_pipeline, "emotion", video_path)

    # =============================
    # FAILURE CHECK
    # =============================
    if failed:
        print("\nOne or more pipelines failed:")
        for name, code in failed:
            print(f" - {name} failed ({code})")
        sys.exit(1)

    print("\nAll pipelines finished successfully")

    # =============================
    # COMBINE
    # =============================
    print("\nRunning combine()...")
    combine_df = combine()

    if combine_df is None or combine_df.empty:
        raise ValueError("Combined dataframe is empty!")

    print("combine() completed")

    # =============================
    # COMPUTE SCORES
    # =============================
    print("\nRunning compute_scores()...")
    result = compute_scores(combine_df)

    if isinstance(result, tuple) and len(result) >= 2:
        df, _ = result
    else:
        df = result

    if df is None or df.empty:
        raise ValueError("Scoring output is empty!")

    print("compute_scores() completed")

    total_time = round(time.time() - start_time, 2)
    print(f"\nFinished Successfully in {total_time}s", flush=True)

    return df


if __name__ == "__main__":
    cv_pipelines()