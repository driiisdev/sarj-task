import sys
import os
import logging
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine

# Add the `server` directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your application config
from config.config import Config

# Interpret the config file for Python logging
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

# Set up target metadata
from app.models.base import Base
target_metadata = Base.metadata

def get_url():
    url = Config.SQLALCHEMY_DATABASE_URI
    logger.info(f"Using URL: {url}")
    return url

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
