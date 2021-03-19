# Global config variables are loaded from env files here
import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
ACCESS_TOKEN_KEY = os.environ.get("ACCESS_TOKEN_KEY")
REFRESH_TOKEN_KEY = os.environ.get("REFRESH_TOKEN_KEY")

SQLALCHEMY_CONNECTION_STRING = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
