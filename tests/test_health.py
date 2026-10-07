"""Tests for the skeleton itself: health check, router wiring and validation.

These assert what is true both now and after the note tickets land — that the
routes exist and are reachable, and that the shared schemas reject bad input —
never the temporary 501 answer of a stub.
"""

from fastapi.testclient import TestClient

from app.config import settings
from app.schemas import NoteCreate


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_docs_and_openapi_are_available(client: TestClient) -> None:
    assert client.get("/docs").status_code == 200

    schema = client.get("/openapi.json").json()
    paths = schema["paths"]
    assert "post" in paths["/notes"]
    assert "get" in paths["/notes"]
    assert "get" in paths["/notes/{id}"]
    assert "delete" in paths["/notes/{id}"]
    assert "get" in paths["/health"]


def test_note_create_trims_titel() -> None:
    assert NoteCreate(titel="  Einkauf  ").titel == "Einkauf"


def test_invalid_payload_is_rejected_with_422(client: TestClient) -> None:
    # The route and its schema contract already reject bad input, before the
    # endpoint body runs and before its ticket lands.
    assert client.post("/notes", json={}).status_code == 422
    assert client.post("/notes", json={"titel": "   "}).status_code == 422
    assert (
        client.post("/notes", json={"titel": "x" * (settings.max_title_length + 1)}).status_code
        == 422
    )
    assert (
        client.post(
            "/notes", json={"titel": "ok", "tags": ["t"] * (settings.max_tags + 1)}
        ).status_code
        == 422
    )
