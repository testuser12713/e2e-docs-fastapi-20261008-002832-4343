"""Tests for ``GET /notes/{id}`` (AC-06, AC-07)."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from app.schemas import Note
from app.storage import repository


def _seed_note() -> Note:
    note = Note(
        id=str(uuid4()),
        titel="Groceries",
        inhalt="Milk, eggs, bread",
        tags=["shopping", "home"],
        erstellt_am=datetime.now(UTC),
    )
    repository.add(note)
    return note


def test_get_note_returns_seeded_note_field_by_field(client: TestClient) -> None:
    seeded = _seed_note()

    response = client.get(f"/notes/{seeded.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == seeded.id
    assert body["titel"] == seeded.titel
    assert body["inhalt"] == seeded.inhalt
    assert body["tags"] == seeded.tags
    assert datetime.fromisoformat(body["erstellt_am"]) == seeded.erstellt_am


def test_get_note_unknown_id_returns_404_with_detail(client: TestClient) -> None:
    response = client.get(f"/notes/{uuid4()}")

    assert response.status_code == 404
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], str)


def test_get_note_returns_latest_state_after_update(client: TestClient) -> None:
    seeded = _seed_note()
    updated = seeded.model_copy(update={"titel": "Updated", "tags": []})
    repository.add(updated)

    response = client.get(f"/notes/{seeded.id}")

    assert response.status_code == 200
    assert response.json()["titel"] == "Updated"
    assert response.json()["tags"] == []


def test_get_note_only_returns_the_requested_note(client: TestClient) -> None:
    first = _seed_note()
    second = Note(
        id=str(uuid4()),
        titel="Second",
        inhalt="Other",
        tags=["work"],
        erstellt_am=datetime.now(UTC) + timedelta(seconds=1),
    )
    repository.add(second)

    response = client.get(f"/notes/{second.id}")

    assert response.status_code == 200
    assert response.json()["id"] == second.id
    assert response.json()["id"] != first.id
