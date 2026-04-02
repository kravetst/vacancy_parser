from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGODB_URI: str
    DB_NAME: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    GOOGLE_SHEET_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
