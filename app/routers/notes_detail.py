"""``GET /notes/{id}`` — fetch a single note. Stub until its own ticket lands."""

from fastapi import APIRouter, HTTPException, status

from app.schemas import Note

router = APIRouter()


@router.get("/notes/{id}", response_model=Note)
def get_note(id: str) -> Note:
    """Return the note with the given id (not implemented yet)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
