"""``GET /notes`` — list notes, optionally filtered by tag."""

from fastapi import APIRouter, Depends, Query

from app.schemas import Note
from app.storage import NoteRepository, get_repository

router = APIRouter()


@router.get("/notes", response_model=list[Note])
def list_notes(
    tag: str | None = Query(default=None),
    repo: NoteRepository = Depends(get_repository),
) -> list[Note]:
    """Return stored notes in creation order, optionally filtered by ``tag``."""
    notes = repo.list()
    if tag is not None:
        notes = [note for note in notes if tag in note.tags]
    return notes
