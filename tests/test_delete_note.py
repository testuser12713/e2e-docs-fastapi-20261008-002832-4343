"""Tests for ``DELETE /notes/{id}`` (AC-08, AC-09)."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.schemas import Note
from app.storage import repository


def _make_note(note_id: str, titel: str) -> Note:
    return Note(
        id=note_id,
        titel=titel,
        inhalt="",
        tags=[],
        erstellt_am=datetime.now(UTC),
    )


def test_delete_stored_note_returns_204_empty_body(client: TestClient) -> None:
    first = _make_note("id-1", "first")
    second = _make_note("id-2", "second")
    repository.add(first)
    repository.add(second)

    response = client.delete("/notes/id-1")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_removes_only_given_note(client: TestClient) -> None:
    first = _make_note("id-1", "first")
    second = _make_note("id-2", "second")
    repository.add(first)
    repository.add(second)

    client.delete("/notes/id-1")

    assert repository.get("id-1") is None
    assert repository.get("id-2") is second
    assert [note.id for note in repository.list()] == ["id-2"]


def test_delete_unknown_note_returns_404_with_detail(client: TestClient) -> None:
    response = client.delete("/notes/does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert "detail" in body
    assert body["detail"]
