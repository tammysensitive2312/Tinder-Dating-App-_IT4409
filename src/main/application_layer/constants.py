# constants.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

# Database Configuration
DB_TYPE = os.getenv("DB_TYPE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

# Database Engine Parameters
DB_ECHO = os.getenv("DB_ECHO", "True").lower() == "true"
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT"))

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
EXPIRATION_TIME = int(os.getenv("EXPIRATION_TIME"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")