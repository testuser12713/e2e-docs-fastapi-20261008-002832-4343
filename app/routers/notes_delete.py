"""``DELETE /notes/{id}`` — remove a note. Stub until its own ticket lands."""

from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: str) -> None:
    """Delete the note with the given id (not implemented yet)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
