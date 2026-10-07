"""``GET /notes/{id}`` — fetch a single note."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import Note
from app.storage import NoteRepository, get_repository

router = APIRouter()


@router.get("/notes/{id}", response_model=Note)
def get_note(id: str, repository: NoteRepository = Depends(get_repository)) -> Note:
    """Return the note with the given id, or 404 if it does not exist."""
    note = repository.get(id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note {id} not found")
    return note
