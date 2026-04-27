import matplotlib.pyplot as plt
import seaborn as sns
from ml.config import FEATURES


def run_eda(df):
    print("\nDataset Shape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nTarget Distribution:")
    print(df["target"].value_counts())

    corr_df = df[FEATURES + ["target"]].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, cmap="Blues", fmt=".2f")
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.show()
