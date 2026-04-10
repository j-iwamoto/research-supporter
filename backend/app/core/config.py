"""設定管理 - 環境変数の読み込み"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""

    # Gemini API
    GEMINI_API_KEY: str = ""

    # Firebase
    FIREBASE_PROJECT_ID: str = ""

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # App
    APP_NAME: str = "Research Manager API"
    DEBUG: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
