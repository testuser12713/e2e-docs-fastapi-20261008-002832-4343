"""In-memory note storage.

Notes live for the lifetime of the process only. The repository keeps a dict
behind a ``threading.Lock`` so concurrent requests cannot corrupt it.
"""

import threading

from app.schemas import Note


class NoteRepository:
    """Thread-safe in-memory store of :class:`~app.schemas.Note` objects."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._notes: dict[str, Note] = {}

    def add(self, note: Note) -> Note:
        """Store ``note`` and return it."""
        with self._lock:
            self._notes[note.id] = note
        return note

    def list(self) -> list[Note]:
        """Return all notes in insertion order."""
        with self._lock:
            return list(self._notes.values())

    def get(self, note_id: str) -> Note | None:
        """Return the note with ``note_id`` or ``None``."""
        with self._lock:
            return self._notes.get(note_id)

    def delete(self, note_id: str) -> bool:
        """Delete the note and report whether it existed."""
        with self._lock:
            return self._notes.pop(note_id, None) is not None

    def clear(self) -> None:
        """Remove every stored note (used by tests)."""
        with self._lock:
            self._notes.clear()


repository = NoteRepository()


def get_repository() -> NoteRepository:
    """FastAPI dependency returning the process-wide repository."""
    return repository
