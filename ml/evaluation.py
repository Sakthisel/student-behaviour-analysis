from sklearn.metrics import accuracy_score, classification_report


def evaluate_model(model, X_test, y_test, model_name):
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)

    print("\n==============================")
    print(f"{model_name} Accuracy: {acc:.4f}")
    print("==============================")

    print(
        classification_report(
            y_test,
            preds,
            labels=[0, 1, 2],
            target_names=["LOW", "MEDIUM", "HIGH"],
            zero_division=0,
        )
    )

    return acc, preds
