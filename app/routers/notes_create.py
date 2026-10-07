"""``POST /notes`` — create a note."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, status

from app.schemas import Note, NoteCreate
from app.storage import NoteRepository, get_repository

router = APIRouter()


@router.post("/notes", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(
    note: NoteCreate,
    repo: NoteRepository = Depends(get_repository),
) -> Note:
    """Validate ``note``, store it and return the stored note.

    FastAPI validates the request body before this body runs, so an invalid
    payload already answers 422 and nothing is stored.
    """
    stored = Note(
        id=str(uuid4()),
        titel=note.titel,
        inhalt=note.inhalt,
        tags=note.tags,
        erstellt_am=datetime.now(UTC),
    )
    return repo.add(stored)
