import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from ml.data_loader import load_data
from ml.preprocessing import clean_data
from ml.eda import run_eda
from ml.transformation import transform_features
from ml.split import split_data
from ml.training import train_ml_models, train_lstm_model
from ml.prediction import predict_hybrid


def main():
    print("\nLoading data...")
    df = load_data()

    print("\nCleaning data...")
    df = clean_data(df)

    print("\nRunning EDA...")
    run_eda(df)

    print("\nTransforming data...")
    X, y, scaler, encoders = transform_features(df)

    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = split_data(X, y)

    print("\nTraining all ML models...")
    train_ml_models(X_train, X_test, y_train, y_test)

    print("\nTraining LSTM model...")
    train_lstm_model(df)

    sample = {
        "joint_visual_attention": 1,
        "individual_attention": 0,
        "looking_other_student": 0,
        "looking_away": 1,
        "head_nod_shake": 0,
        "confidence": 0.85,
        "fiddling": 1,
        "touching_tool": 0,
    }

    print("\nHybrid Prediction:")
    print(predict_hybrid(sample))

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
