from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.models import item, user  # noqa: F401

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def ensure_catalog_schema() -> None:
    inspector = inspect(engine)
    if "items" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("items")}
    column_definitions = {
        "slug": "VARCHAR(120)",
        "name": "VARCHAR(200)",
        "symptoms": "JSON",
        "uses": "JSON",
        "safety_notes": "JSON",
    }
    missing_columns = set(column_definitions) - columns

    if not missing_columns:
        return

    with engine.begin() as connection:
        for column in missing_columns:
            column_type = column_definitions[column]
            connection.execute(text(f"ALTER TABLE items ADD COLUMN {column} {column_type} NULL"))

        if "title" in columns:
            connection.execute(text("UPDATE items SET name = title WHERE name IS NULL"))
        connection.execute(text("UPDATE items SET name = CONCAT('Catalog item ', id) WHERE name IS NULL"))
        connection.execute(text("UPDATE items SET slug = CONCAT('legacy-item-', id) WHERE slug IS NULL"))
        for column in ("symptoms", "uses", "safety_notes"):
            connection.execute(text(f"UPDATE items SET {column} = '[]' WHERE {column} IS NULL"))
