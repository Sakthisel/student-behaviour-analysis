PRE_TRAINED_MODEL = "google/flan-t5-small"
OUTPUT_DIR = "models/llm_finetuned"
DATA_PATH = "llm/data/student_reports.jsonl"

NUM_EPOCHS = 1
BATCH_SIZE = 1
LEARNING_RATE = 1e-5

MAX_INPUT_LENGTH = 256
MAX_TARGET_LENGTH = 128