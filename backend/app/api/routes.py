from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.file_service import save_uploaded_video
from app.services.pipeline_service import run_analysis_pipeline
from app.schemas.response import AnalyzeResponse


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(file: UploadFile = File(...)):
    try:
        video_path = save_uploaded_video(file)
        result = run_analysis_pipeline(video_path)
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
