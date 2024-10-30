"""
Main application entry point for the Project Gutenberg Analysis API.
This module initializes the FastAPI application with all necessary middleware and routes.
"""
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

# Local imports
from app.routes import health, books, analysis
from config.config import Config
from config.db import engine

# Initialize FastAPI application
app = FastAPI(
    title="Project Gutenberg Analysis API",
    debug=True
)

###################
# Logging Setup
###################
def setup_logging():
    """Configure application logging with rotating file handler"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configure rotating file handler
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    file_handler.setLevel(logging.INFO)

    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    logger.info('App startup')

setup_logging()

###################
# Middleware Setup
###################
# Initialize rate limiter
limiter = FixedWindowRateLimiter(storage=MemoryStorage())

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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

# Rate limiting configuration
app.add_middleware(
    RateLimitingMiddleware,
    strategy=limiter,
)

###################
# Startup Events
###################
@app.on_event("startup")
async def startup_event():
    """
    Handles application startup tasks:
    - Prints startup confirmation
    - Checks database connection
    - Runs database migrations
    """
    print(f"App starting")
    
    # Test database connection
    try:
        with engine.connect() as conn:
            logging.info("Database connected successfully!")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
    
    print(f"App started successfully")
    
    # Run database migrations
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
###################
# Route Registration
###################
# Register API routes with their respective prefixes
app.include_router(health.router, prefix="/api/health")
app.include_router(books.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")

# Set global rate limit
limit(app, "15/minute")

# Make the app importable
__all__ = ["app"]
from app import app
