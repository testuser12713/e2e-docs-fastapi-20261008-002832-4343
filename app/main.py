"""FastAPI application entry point.

The four note routers are stubs until their own tickets land; ``/health``
answers immediately so the service is startable and probeable from day one.
"""

from fastapi import FastAPI

from app.config import settings
from app.routers import notes_create, notes_delete, notes_detail, notes_list

app = FastAPI(title=settings.app_name)

app.include_router(notes_create.router)
app.include_router(notes_list.router)
app.include_router(notes_detail.router)
app.include_router(notes_delete.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}
