import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
  HOST = os.getenv('HOST')
  PORT = int(os.getenv('PORT'))
  SECRET_KEY = os.getenv('SECRET_KEY')
  FRONTEND_ORIGIN=os.getenv('FRONTEND_ORIGIN')
  DB_HOST = os.getenv('DB_HOST')
  DB_NAME = os.getenv('DB_NAME')
  DB_USERNAME = os.getenv('DB_USERNAME')
  DB_PASSWORD = os.getenv('DB_PASSWORD')
  SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  GUTENBERG_CONTENT_URL=os.getenv('GUTENBERG_CONTENT_URL')
  GUTENBERG_METADATA_URL=os.getenv('GUTENBERG_METADATA_URL')
  LANGUAGES = ['en-US', 'en-GB', 'en-CA', 'es']
