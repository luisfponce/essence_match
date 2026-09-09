from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.session import SessionLocal, ensure_catalog_schema, init_db
from app.services.catalog_seed import seed_catalog


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    ensure_catalog_schema()
    with SessionLocal() as session:
        seed_catalog(session)
    yield


app = FastAPI(title=settings.project_name, version="0.1.0", lifespan=lifespan)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": settings.project_name, "docs": "/docs"}


app.include_router(api_router, prefix=settings.api_v1_prefix)
