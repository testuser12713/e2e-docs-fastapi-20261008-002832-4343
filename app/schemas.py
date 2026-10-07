"""Pydantic v2 models for the notes API.

Uses only Pydantic v2 APIs: ``model_config = ConfigDict(...)`` and
``field_validator``. No ``@validator``, no inner ``class Config``.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.config import settings


class NoteCreate(BaseModel):
    """Payload accepted by ``POST /notes``."""

    model_config = ConfigDict(str_strip_whitespace=False)

    titel: str
    inhalt: str = ""
    tags: list[str] = Field(default_factory=list)

    @field_validator("titel")
    @classmethod
    def validate_titel(cls, value: str) -> str:
        """Trim the title and require 1..max_title_length characters."""
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("titel must not be empty or whitespace only")
        if len(trimmed) > settings.max_title_length:
            raise ValueError(
                f"titel must not be longer than {settings.max_title_length} characters"
            )
        return trimmed

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        """Reject more than ``settings.max_tags`` tags."""
        if len(value) > settings.max_tags:
            raise ValueError(f"at most {settings.max_tags} tags are allowed")
        return value


class Note(BaseModel):
    """A stored note as returned by the API."""

    model_config = ConfigDict(str_strip_whitespace=False)

    id: str
    titel: str
    inhalt: str = ""
    tags: list[str] = Field(default_factory=list)
    erstellt_am: datetime
