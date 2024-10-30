import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from pydantic import BaseModel as PydanticBase

Base = declarative_base()

class BaseModel(Base):
  __abstract__ = True

  @declared_attr
  def __tablename__(cls):
    return cls.__name__.lower()

  id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))

  def __init__(self, *args, **kwargs):
    if kwargs:
      for key, value in kwargs.items():
        if key != "__class__":
          setattr(self, key, value)
    super().__init__(*args, **kwargs)

  def __repr__(self):
    return f"<{self.__class__.__name__}(id={self.id})>"

  def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  def save(self, session):
    session.add(self)
    session.commit()

  def delete(self, session):
    session.delete(self)
    session.commit()


class PydanticBaseModel(PydanticBase):
  class Config:
    from_attributes = True
    json_encoders = {
      int: str 
    }

    @classmethod
    def from_orm(cls, obj):
      data = {field: getattr(obj, field) for field in cls.__fields__ if hasattr(obj, field)}
      data['id'] = str(data['id'])
      return cls(**data)
