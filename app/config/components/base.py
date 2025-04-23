from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import ENV_FILE_PATH


class BaseConfig(BaseSettings):
    env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    workers: int = 1
    reload: bool = True

    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
    )
