"""Configuration settings for the auth service"""

import os
from pathlib import Path


class Settings:
    """Configuration settings for the auth service"""

    def __init__(self):
        # pylint: disable=invalid-name

        # Get project root directory
        project_root = Path(__file__).resolve().parents[1]
        keys_dir = project_root / "keys"

        # ------------- Authentication Config -------------
        self.AUTH_URL: str = os.getenv("AUTH_URL", "http://localhost:9000")
        # ------------- Authentication Config -------------

        # ------------- MongoDB Config -------------
        self.MONGO_URI: str = os.getenv(
            "MONGO_URI",
            "mongodb://127.0.0.1:27017/?directConnection=true&"
            "serverSelectionTimeoutMS=2000&appName=mongosh+2.3.9",
        )
        self.DB_NAME: str = os.getenv("DB_NAME", "test")
        self.POSTS_COLLECTION: str = os.getenv("POSTS_COLLECTION", "posts")
        # ------------- MongoDB Config -------------

        # ------------- JWT Config -------------
        with open(keys_dir / "public.pem") as key_file:
            self.JWT_PUBLIC_KEY: str = key_file.read()
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
        self.JWT_ISSUER: str = os.getenv(
            "JWT_ISSUER",
            "awesome-babushka-auth-service",
        )
        self.JWT_AUDIENCE: str = os.getenv(
            "JWT_AUDIENCE",
            "awesome-babushka-users",
        )

        self.SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret_key")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )
        self.ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        # ------------- JWT Config -------------

        # ------------- Email Config -------------
        self.ENABLE_EMAIL: bool = (
            os.getenv("ENABLE_EMAIL", "false").lower() == "true"
        )
        self.NO_REPLY_EMAIL: str = os.getenv(
            "NO_REPLY_EMAIL", "noreply@awesomebabushka.com"
        )
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "172.18.0.1")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
        self.HOST_NAME: str = "localhost:8000"
        # ------------- Email Config -------------

        # ------------- MiniO Config -------------
        self.MINIO_ENDPOINT = os.getenv(
            "MINIO_ENDPOINT", "http://localhost:9000"
        )
        self.MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.MINIO_BUCKET = os.getenv("MINIO_BUCKET", "awesome-babushka")
        # ------------- MiniO Config -------------


settings = Settings()
