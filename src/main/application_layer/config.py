import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv


class Config:
    """Class đọc và quản lý các cấu hình từ file .env"""

    def __init__(self, env_file: Optional[str] = None):
        """
        Khởi tạo các cấu hình từ file .env

        Args:
            env_file: Đường dẫn tới file .env. Mặc định sẽ tìm file .env trong thư mục hiện tại.
        """
        load_dotenv(dotenv_path=env_file)

        # Database configurations
        self.DB_TYPE = os.getenv('DB_TYPE')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = int(os.getenv('DB_PORT'))
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_DRIVER = os.getenv('DB_DRIVER')

        # Database engine configurations
        self.DB_ECHO = self._parse_bool(os.getenv('DB_ECHO'))
        self.DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE'))
        self.DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW'))
        self.DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT'))


    def _parse_bool(self, value: str) -> bool:
        """Convert string value to boolean"""
        return value.lower() in ('true', 'yes', '1', 't', 'y')

    def as_dict(self) -> Dict[str, Any]:
        """Chuyển các cấu hình thành dictionary"""
        return {
            'DB_TYPE': self.DB_TYPE,
            'DB_HOST': self.DB_HOST,
            'DB_PORT': self.DB_PORT,
            'DB_USER': self.DB_USER,
            'DB_PASSWORD': self.DB_PASSWORD,
            'DB_NAME': self.DB_NAME,
            'DB_DRIVER': self.DB_DRIVER,
            'DB_ECHO': self.DB_ECHO,
            'DB_POOL_SIZE': self.DB_POOL_SIZE,
            'DB_MAX_OVERFLOW': self.DB_MAX_OVERFLOW,
            'DB_POOL_TIMEOUT': self.DB_POOL_TIMEOUT,
        }