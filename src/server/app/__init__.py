import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from limits.aio.storage import MemoryStorage
from limits.aio.strategies import FixedWindowRateLimiter
from fastlimits import RateLimitingMiddleware, limit
from alembic.config import Config as AlembicConfig
from alembic import command

from app.routes import health, books, analysis
from config.config import Config
from config.db import engine


app = FastAPI(
    title="Project Gutenberg Analysis API"
)

def setup_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs', exists_ok=True)

    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    logger.info('App startup')

setup_logging()


limiter = FixedWindowRateLimiter(storage=MemoryStorage())

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Accept-Language",
        "Accept-Encoding",
    ],
)

app.add_middleware(
    RateLimitingMiddleware,
    strategy=limiter,
)

@app.on_event("startup")
async def startup_event():
    print(f"App starting")
    
    try:
        with engine.connect() as conn:
            logging.info("Database connected successfully!")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        
    
    print(f"App started successfully")
    
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    

app.include_router(health.router, prefix="/api/health")
app.include_router(books.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")

limit(app, "15/minute")

from app import app
