"""Shared pytest fixtures for the notes API tests."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import repository


@pytest.fixture(autouse=True)
def _empty_repository() -> Iterator[None]:
    """Clear the in-memory repository before and after every test."""
    repository.clear()
    yield
    repository.clear()


@pytest.fixture
def client() -> TestClient:
    """A TestClient bound to the application."""
    return TestClient(app)
