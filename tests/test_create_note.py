"""Tests for ``POST /notes`` (create a note)."""

from datetime import datetime

from fastapi.testclient import TestClient

from app.storage import repository


def test_create_full_body_returns_201(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "Erster Eintrag", "inhalt": "Inhalt", "tags": ["a", "b"]},
    )
    assert response.status_code == 201

    body = response.json()
    assert body["id"]
    assert body["titel"] == "Erster Eintrag"
    assert body["inhalt"] == "Inhalt"
    assert body["tags"] == ["a", "b"]

    created = datetime.fromisoformat(body["erstellt_am"])
    assert created.tzinfo is not None
    assert created.utcoffset() is not None

    stored = repository.get(body["id"])
    assert stored is not None
    assert stored.id == body["id"]


def test_create_ids_are_unique(client: TestClient) -> None:
    first = client.post("/notes", json={"titel": "Eins"})
    second = client.post("/notes", json={"titel": "Zwei"})
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]


def test_create_omitted_content_and_tags_default(client: TestClient) -> None:
    response = client.post("/notes", json={"titel": "Nur Titel"})
    assert response.status_code == 201

    body = response.json()
    assert body["inhalt"] == ""
    assert body["tags"] == []


def test_create_exactly_five_tags_accepted(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "Fünf Tags", "tags": ["a", "b", "c", "d", "e"]},
    )
    assert response.status_code == 201
    assert response.json()["tags"] == ["a", "b", "c", "d", "e"]


def test_create_six_tags_rejected_and_nothing_stored(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "Zu viele Tags", "tags": ["a", "b", "c", "d", "e", "f"]},
    )
    assert response.status_code == 422
    assert repository.list() == []


def test_create_missing_title_rejected_and_nothing_stored(client: TestClient) -> None:
    response = client.post("/notes", json={"inhalt": "ohne Titel"})
    assert response.status_code == 422
    assert repository.list() == []


def test_create_empty_title_rejected_and_nothing_stored(client: TestClient) -> None:
    response = client.post("/notes", json={"titel": ""})
    assert response.status_code == 422
    assert repository.list() == []


def test_create_whitespace_title_rejected_and_nothing_stored(client: TestClient) -> None:
    response = client.post("/notes", json={"titel": "   "})
    assert response.status_code == 422
    assert repository.list() == []


def test_create_too_long_title_rejected_and_nothing_stored(client: TestClient) -> None:
    response = client.post("/notes", json={"titel": "x" * 101})
    assert response.status_code == 422
    assert repository.list() == []


def test_create_hundred_char_title_accepted(client: TestClient) -> None:
    response = client.post("/notes", json={"titel": "x" * 100})
    assert response.status_code == 201
    assert len(response.json()["titel"]) == 100
