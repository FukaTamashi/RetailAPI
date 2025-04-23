from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from config.constants import ENV_FILE_PATH

class ComponentsConfig(BaseSettings):
    api_key:    str = Field(..., env="API_KEY")
    base_url:   str = Field(..., env="BASE_URL")
    site_code:  str = Field(..., env="SITE_CODE")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
    )

__all__ = ["ComponentsConfig"]