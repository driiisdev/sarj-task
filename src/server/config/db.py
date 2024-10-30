from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from sqlalchemy.exc import SQLAlchemyError
from config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(session_factory)
Base = declarative_base()
Base.query = SessionLocal.query_property()


class DatabaseManager:
    @staticmethod
    @contextmanager
    def get_db() -> Generator:
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def create_all():
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def drop_all():
        Base.metadata.drop_all(bind=engine)


class DBStorage:
    @staticmethod
    def _get_db():
        return SessionLocal()

    @staticmethod
    def all(cls=None):
        db = DBStorage._get_db()
        try:
            if cls is None:
                result = db.query(Base).all()
            else:
                result = db.query(cls).all()
            for obj in result:
                db.expunge(obj)
                db.enable_relationship_loading(obj)
            return result
        finally:
            db.close()

    @staticmethod
    def get(cls, id):
        db = DBStorage._get_db()
        try:
            obj = db.query(cls).filter(cls.id == id).first()
            if obj:
                db.expunge(obj)
                db.enable_relationship_loading(obj)
            return obj
        finally:
            db.close()

    @staticmethod
    def new(obj):
        with DatabaseManager.get_db() as db:
            db.add(obj)
            db.flush()
            for attr in obj.__dict__:
                if not attr.startswith('_'):
                    getattr(obj, attr)
            db.expunge(obj)
            db.enable_relationship_loading(obj)
            return obj

    @staticmethod
    def delete(obj=None):
        if obj is not None:
            with DatabaseManager.get_db() as db:
                db.delete(obj)
    