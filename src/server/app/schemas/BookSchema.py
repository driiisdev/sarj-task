from app.models.base import PydanticBaseModel
from typing import Optional

class BookSchema(PydanticBaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]
    type: Optional[str]
    image: Optional[str]
    url: Optional[str]
    site_name: Optional[str]
    content: Optional[str]
