from datetime import datetime, UTC
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, JSON, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CatalogDocument(Base):
    __tablename__ = "catalog_documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_pdf: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)
    extraction_version: Mapped[str] = mapped_column(Text, default="0.1.0", nullable=False)
    doc_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=lambda: {}, nullable=False)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="catalog_document", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (Index("idx_products_name", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    catalog_document_id: Mapped[int] = mapped_column(
        ForeignKey("catalog_documents.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    scientific_name: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    category: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingredients: Mapped[list[str]] = mapped_column(JSON, default=lambda: [], nullable=False)
    usage_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    usage_modes: Mapped[list[str]] = mapped_column(JSON, default=lambda: [], nullable=False)
    seasonal: Mapped[bool] = mapped_column(default=False, nullable=False)
    image_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    source_document_name: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    source_page: Mapped[int | None] = mapped_column(nullable=True, index=True)
    source_card_bbox: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    extraction_confidence: Mapped[float | None] = mapped_column(nullable=True)
    warnings: Mapped[list[str]] = mapped_column(JSON, default=lambda: [], nullable=False)
    derived_tags: Mapped[list[str]] = mapped_column(JSON, default=lambda: [], nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        onupdate=lambda: datetime.now(UTC),
    )

    catalog_document: Mapped["CatalogDocument"] = relationship(back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (
        Index("idx_product_variants_sku_not_null", "sku", unique=True, postgresql_where=text("sku IS NOT NULL")),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )
    sku: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    size_value: Mapped[float | None] = mapped_column(nullable=True)
    size_unit: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_size: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    product: Mapped["Product"] = relationship(back_populates="variants")
