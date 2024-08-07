import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

TIME_EXPIRE = int(os.environ.get("TIME_EXPIRE"))
MAX_LENGTH = int(os.environ.get("MAX_LENGTH"))
MAX_LENGTH *= MAX_LENGTH

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.environ.get("ALGORITHM")
JWT_SECRET = os.environ.get("JWT_SECRET")
