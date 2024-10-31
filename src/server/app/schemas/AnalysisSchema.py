from app.models.base import PydanticBaseModel

class AnalysisResponse(PydanticBaseModel):
    success: bool
    data: dict

class CharacterAnalysis(PydanticBaseModel):
    characters: list[dict[str, str]]

class LanguageAnalysis(PydanticBaseModel):
    language_code: str
    confidence: float

class SentimentAnalysis(PydanticBaseModel):
    sentiment: float
    classification: str

class BookSummary(PydanticBaseModel):
    summary: str
    word_count: int
