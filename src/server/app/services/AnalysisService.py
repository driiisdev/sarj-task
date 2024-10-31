import logging
from textblob import TextBlob
from langdetect import detect

from app.services import BookService
from app.schemas.AnalysisSchema import AnalysisResponse
from app.utils.llm import analyze_with_llm

logger = logging.getLogger(__name__)

async def analyze_characters(book_id: str) -> AnalysisResponse:
    book = await BookService.get_book(book_id)
    if not book:
        raise ValueError(f"Book {book_id} not found")
    
    try:
        characters = await analyze_with_llm(book.content, "Identify key characters in this text")
        return {
            "success": True,
            "data": {"characters": characters}
        }
    except Exception as e:
        logger.error(f"Character analysis failed for book {book_id}: {str(e)}")
        raise ValueError(f"Character analysis failed for book {book_id}: {str(e)}")

async def detect_language(book_id: str) -> AnalysisResponse:
    book = await BookService.get_book(book_id)
    if not book:
        raise ValueError(f"Book {book_id} not found")
    
    try:
        languageCode = detect(book.content)
        return {
            "success": True,
            "data": {
                "language_code": languageCode,
                "confidence": 0.9
            }
        }
    except Exception as e:
        logger.error(f"Unexpected error in language detection for book {book_id}: {str(e)}")
        raise ValueError(f"Unexpected error in language detection for book {book_id}: {str(e)}")

async def analyze_sentiment(book_id: str) -> AnalysisResponse:
    book = await BookService.get_book(book_id)
    if not book:
        raise ValueError(f"Book {book_id} not found")
    
    try:
        blob = TextBlob(book.content)
        sentiment = blob.sentiment.polarity
        
        if sentiment > 0.1:
            classification = "positive"
        elif sentiment < -0.1:
            classification = "negative"
        else:
            classification = "neutral"
            
        return {
            "success": True,
            "data": {
                "sentiment": sentiment,
                "classification": classification
            }
        }
    except Exception as e:
        logger.error(f"Sentiment analysis failed for book {book_id}: {str(e)}")
        raise ValueError(f"Sentiment analysis failed for book {book_id}: {str(e)}")

async def generate_summary(book_id: str) -> AnalysisResponse:
    book = await BookService.get_book(book_id)
    if not book:
        raise ValueError(f"Book {book_id} not found")

    try:
        summary = await analyze_with_llm(book.content, "Generate a plot summary for this book")
        return {
            "success": True,
            "data": {
                "summary": summary,
                "word_count": len(summary.split())
            }
        }
    except Exception as e:
        logger.error(f"Summary generation failed for book {book_id}: {str(e)}")
        raise ValueError(f"Summary generation failed for book {book_id}: {str(e)}")
    