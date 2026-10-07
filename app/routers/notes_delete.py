"""``DELETE /notes/{id}`` — remove a note."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.storage import NoteRepository, get_repository

router = APIRouter()


@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: str, repo: NoteRepository = Depends(get_repository)) -> None:
    """Delete the note with the given id.

    Returns ``204`` with an empty body when the note existed,
    otherwise ``404`` with a JSON ``detail`` body.
    """
    if not repo.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
