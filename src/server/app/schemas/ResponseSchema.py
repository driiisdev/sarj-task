from app.models.base import PydanticBaseModel

class SuccessResponse(PydanticBaseModel):
    message: str
    status: str="success"
    

class ErrorResponse(PydanticBaseModel):
    message: str
    status: str="error"
