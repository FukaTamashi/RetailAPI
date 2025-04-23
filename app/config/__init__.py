from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.components import ComponentsConfig
from config.constants import ENV_FILE_PATH
from config.envs.development import DevelopmentConfig


class Settings(BaseSettings):
    env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int     = Field(..., env="APP_PORT")
    workers: int      = Field(..., env="WORKERS")
    reload: bool      = True

    docs_url: str     = "/docs"
    redoc_url: str    = "/redoc"
    cors_origins: list[str]           = ["*"]
    cors_allow_credentials: bool      = True
    cors_allow_methods: list[str]     = ["*"]
    cors_allow_headers: list[str]     = ["*"]

    api_key:   str    = Field(..., env="API_KEY")
    base_url:  str    = Field(..., env="BASE_URL")
    site_code: str    = Field(..., env="SITE_CODE")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
    )

settings = Settings()