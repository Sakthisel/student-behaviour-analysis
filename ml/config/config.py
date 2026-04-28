DATA_PATH = "./outputs/csv/final_combined.csv"
MODEL_DIR = "models/ml_trained_models"

FEATURES = [
    "joint_visual_attention",
    "individual_attention",
    "looking_other_student",
    "looking_away",
    "head_nod_shake",
    "confidence",
    "fiddling",
    "touching_tool",
]

TARGET_COL = "engagement_score"

LABEL_MAP = {
    0: "LOW",
    1: "MEDIUM",
    2: "HIGH",
}

SEQ_LEN = 10
