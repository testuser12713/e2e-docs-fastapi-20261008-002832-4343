"""``POST /notes`` — create a note. Stub until its own ticket lands."""

from fastapi import APIRouter, HTTPException, status

from app.schemas import Note, NoteCreate

router = APIRouter()


@router.post("/notes", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(note: NoteCreate) -> Note:
    """Create a new note (not implemented yet).

    FastAPI validates the request body before this body runs, so an invalid
    payload already answers 422 and nothing is stored.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
