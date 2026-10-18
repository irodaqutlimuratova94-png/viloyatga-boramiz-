from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/viloyatga_bорамiz"
    secret_key: str = "dev-only-change-me"
    trial_days: int = 30
    telegram_bot_token: str = ""
    web_origin: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
