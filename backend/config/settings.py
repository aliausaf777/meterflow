from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"

    # MySQL
    DB_HOST:     str = "localhost"
    DB_PORT:     int = 3306
    DB_USER:     str = "meterflow_user"
    DB_PASSWORD: str = "ausaf"
    DB_NAME:     str = "meterflow"

    # MongoDB
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB:  str = "meterflow"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # JWT
    SECRET_KEY: str = "meterflow-secret-key-change-in-production"

    # Razorpay
    RAZORPAY_KEY_ID:     str = ""
    RAZORPAY_KEY_SECRET: str = ""

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()