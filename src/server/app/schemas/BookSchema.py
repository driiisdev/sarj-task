from app.models.base import PydanticBaseModel

class BookSchema(PydanticBaseModel):
    id: str
    title: str
    description: str
    type: str
    image: str
    url: str
    site_name: str
    content: str
