from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProductVariantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    sku: str | None = None
    size_value: float | None = None
    size_unit: str | None = None
    raw_size: str | None = None
    created_at: datetime


class ProductVariantCreate(BaseModel):
    sku: str | None = None
    size_value: float | None = None
    size_unit: str | None = None
    raw_size: str | None = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    catalog_document_id: int
    name: str
    scientific_name: str | None = None
    category: str | None = None
    description: str | None = None
    ingredients: list[str] = []
    usage_text: str | None = None
    usage_modes: list[str] = []
    seasonal: bool = False
    image_metadata: dict[str, Any] | None = None
    source_document_name: str | None = None
    source_page: int | None = None
    source_card_bbox: list[float] | None = None
    raw_text: str | None = None
    extraction_confidence: float | None = None
    warnings: list[str] = []
    derived_tags: list[str] = []
    created_at: datetime
    updated_at: datetime
    variants: list[ProductVariantRead] = []


class ProductCreate(BaseModel):
    name: str
    scientific_name: str | None = None
    category: str | None = None
    description: str | None = None
    ingredients: list[str] = []
    usage_text: str | None = None
    usage_modes: list[str] = []
    seasonal: bool = False
    image_metadata: dict[str, Any] | None = None
    source_document_name: str | None = None
    source_page: int | None = None
    source_card_bbox: list[float] | None = None
    raw_text: str | None = None
    extraction_confidence: float | None = None
    warnings: list[str] = []
    derived_tags: list[str] = []
    variants: list[ProductVariantCreate] = []


class CatalogDocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_pdf: str | None = None
    source_hash: str
    extraction_version: str = "0.1.0"
    doc_metadata: dict[str, Any] = {}
    raw_payload: dict[str, Any] | None = None
    imported_at: datetime
    product_count: int = 0