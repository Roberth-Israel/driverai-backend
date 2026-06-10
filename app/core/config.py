from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DriverAI Pro"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./driverai_pro.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    GOOGLE_MAPS_API_KEY: str = ""
    GOOGLE_GEOLOCATION_API_KEY: str = ""

    FIREBASE_CREDENTIALS_PATH: str = ""

    ML_MODEL_PATH: str = "app/ml/models"
    PREDICTION_INTERVAL_MINUTES: int = 60

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
