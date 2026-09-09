from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    symptoms: list[str] = Field(default_factory=list)
    uses: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)


class ItemUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1)
    symptoms: list[str] | None = None
    uses: list[str] | None = None
    safety_notes: list[str] | None = None


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str
    symptoms: list[str]
    uses: list[str]
    safety_notes: list[str]
    created_at: datetime
