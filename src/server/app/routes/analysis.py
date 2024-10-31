from fastapi import APIRouter

from app.controllers import AnalysisController
from app.schemas.AnalysisSchema import (AnalysisResponse)

router = APIRouter()

@router.post("/characters", response_model=AnalysisResponse)
async def analyze_characters(book_id: str):
    return await AnalysisController.analyze_characters(book_id)

@router.post("/language", response_model=AnalysisResponse)
async def detect_language(book_id: str):
    return await AnalysisController.detect_language(book_id)

@router.post("/sentiment", response_model=AnalysisResponse)
async def analyze_sentiment(book_id: str):
    return await AnalysisController.analyze_sentiment(book_id)

@router.post("/summary", response_model=AnalysisResponse)
async def generate_summary(book_id: str):
    return await AnalysisController.generate_summary(book_id)
