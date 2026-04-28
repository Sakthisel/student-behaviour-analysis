from ultralytics import YOLO


def train_model(model_path, data_yaml_path, output_path):
    print("Starting Training...\n")

    model = YOLO(str(model_path))

    model.train(
        data=str(data_yaml_path),
        epochs=50,
        imgsz=640,
        batch=16,
        conf=0.25,
        project=str(output_path / "runs"),
        name="trained_model",
    )

    print("\nTraining completed!\n")
    return model
