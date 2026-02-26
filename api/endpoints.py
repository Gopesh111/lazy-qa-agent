import os
import logging
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import UploadResponse
from core.vision_parser import VideoAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()
UPLOAD_DIR = os.getenv("MEDIA_UPLOAD_DIR", "./temp_media")

@router.post("/analyze-video", response_model=UploadResponse)
async def analyze_bug_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a video.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    trace_id = str(uuid.uuid4())[:8]
    file_path = os.path.join(UPLOAD_DIR, f"{trace_id}_{file.filename}")

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            
        report = await VideoAnalyzer.extract_and_analyze(file_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        return UploadResponse(
            status="success",
            filename=file.filename,
            message="Media parsed and highly structured engineering report generated.",
            report=report
        )

    except Exception as e:
        logger.error(f"Failed to process video: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during video analysis.")