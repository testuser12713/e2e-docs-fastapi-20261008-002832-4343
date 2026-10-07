"""``GET /notes`` — list notes, optionally filtered by tag. Stub for now."""

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas import Note

router = APIRouter()


@router.get("/notes", response_model=list[Note])
def list_notes(tag: str | None = Query(default=None)) -> list[Note]:
    """Return stored notes, optionally only those carrying ``tag``."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
