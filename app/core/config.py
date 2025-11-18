from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    PROJECT_NAME: str = "FastAPI Base"
    DATABASE_URL: str = "sqlite:////data/app.db"


settings = Settings()
