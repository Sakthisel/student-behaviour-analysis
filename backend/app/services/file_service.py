from pathlib import Path
from fastapi import UploadFile
import shutil
import uuid

from app.core.config import UPLOAD_DIR


ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi"}


def save_uploaded_video(file: UploadFile) -> Path:
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported video format. Use .mp4, .mov, or .avi")

    file_name = f"{uuid.uuid4()}{suffix}"
    file_path = UPLOAD_DIR / file_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path
