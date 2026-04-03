from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    api_base_url: str = "http://backend:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
