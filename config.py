import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/tinder-clone')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
    JWT_SECRET_KEY = "your_jwt_secret_key"  # Dùng để mã hóa token JWT
