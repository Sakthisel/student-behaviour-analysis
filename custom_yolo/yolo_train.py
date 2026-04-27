from ultralytics import YOLO


def train_model(model, obj, output_path):
    print("Starting Training...\n")

    model = YOLO(str(model))

    model.train(
        data=str(obj),
        epochs=5,
        imgsz=640,
        batch=16,
        conf=0.25,
        project=str(output_path / "runs"),
        name="trained_model",
    )

    print("\nTraining completed!\n")
    return model
