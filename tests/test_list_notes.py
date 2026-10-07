"""Tests for ``GET /notes`` including the optional tag filter."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.schemas import Note
from app.storage import repository


def _seed(titel: str, tags: list[str]) -> Note:
    """Create a note through the repository and return it."""
    note = Note(
        id=str(uuid4()),
        titel=titel,
        inhalt="",
        tags=tags,
        erstellt_am=datetime.now(UTC),
    )
    return repository.add(note)


def test_empty_store_returns_empty_list(client: TestClient) -> None:
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []


def test_notes_are_returned_in_creation_order(client: TestClient) -> None:
    first = _seed("first", [])
    second = _seed("second", [])
    third = _seed("third", [])

    response = client.get("/notes")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [first.id, second.id, third.id]


def test_tag_filter_returns_only_matching_notes(client: TestClient) -> None:
    work = _seed("work", ["arbeit", "wichtig"])
    _seed("home", ["privat"])
    errand = _seed("errand", ["arbeit"])

    response = client.get("/notes", params={"tag": "arbeit"})
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [work.id, errand.id]


def test_tag_filter_requires_exact_match(client: TestClient) -> None:
    _seed("work", ["arbeit"])

    response = client.get("/notes", params={"tag": "arb"})
    assert response.status_code == 200
    assert response.json() == []


def test_unknown_tag_returns_200_with_empty_list(client: TestClient) -> None:
    _seed("work", ["arbeit"])

    response = client.get("/notes", params={"tag": "does-not-exist"})
    assert response.status_code == 200
    assert response.json() == []
