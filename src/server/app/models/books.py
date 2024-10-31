from sqlalchemy import Column, String, Text

from app.models.base import BaseModel


class Book(BaseModel):
    __tablename__ = "books"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String, nullable=True)
    image = Column(String, nullable=True)
    url = Column(String, nullable=False)
    site_name = Column(String, nullable=True)
    content = Column(Text, nullable=True)
