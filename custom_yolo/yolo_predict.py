def run_inference(video, model, output_path):
    print("Running Inference...\n")

    results = model.predict(
        source=str(video),
        conf=0.03,
        imgsz=416,
        vid_stride=2,
        save=True,
        project=str(output_path / "runs"),
        name="inference_results",
    )

    print("\nInference completed!")
    return results
