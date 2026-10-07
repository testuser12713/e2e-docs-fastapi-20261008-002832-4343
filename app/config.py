"""Application configuration.

Every value is read through ``pydantic-settings`` and can be overridden with an
environment variable of the same (upper-cased) name, e.g. ``APP_NAME``,
``MAX_TAGS`` or ``MAX_TITLE_LENGTH``. All values carry a working default, so the
app boots with no environment variable set.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the notes API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Notes API"
    max_tags: int = 5
    max_title_length: int = 100


settings = Settings()
