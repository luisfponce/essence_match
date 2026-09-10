"""Add catalog schema

Revision ID: 20260910100000_catalog
Revises: 
Create Date: 2026-09-10 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260910100000_catalog"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "catalog_documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("source_pdf", sa.Text, nullable=True),
        sa.Column("source_hash", sa.Text, nullable=False),
        sa.Column("extraction_version", sa.Text, nullable=False, server_default="0.1.0"),
        sa.Column("doc_metadata", postgresql.JSONB, nullable=False, server_default=sa.text("'{}'")),
        sa.Column("raw_payload", postgresql.JSONB, nullable=True),
        sa.Column("imported_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_hash", name="uq_catalog_documents_source_hash"),
    )
    op.create_index("idx_catalog_documents_imported_at", "catalog_documents", ["imported_at"])

    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("catalog_document_id", sa.Integer, sa.ForeignKey("catalog_documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("scientific_name", sa.Text, nullable=True),
        sa.Column("category", sa.Text, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("ingredients", postgresql.JSONB, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("usage_text", sa.Text, nullable=True),
        sa.Column("usage_modes", postgresql.JSONB, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("seasonal", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("image_metadata", postgresql.JSONB, nullable=True),
        sa.Column("source_document_name", sa.Text, nullable=True),
        sa.Column("source_page", sa.Integer, nullable=True),
        sa.Column("source_card_bbox", postgresql.JSONB, nullable=True),
        sa.Column("raw_text", sa.Text, nullable=True),
        sa.Column("extraction_confidence", sa.Float, nullable=True),
        sa.Column("warnings", postgresql.JSONB, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("derived_tags", postgresql.JSONB, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_products_catalog_document_id", "products", ["catalog_document_id"])
    op.create_index("idx_products_name", "products", ["name"])
    op.create_index("idx_products_category", "products", ["category"])

    op.create_table(
        "product_variants",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sku", sa.Text, nullable=True),
        sa.Column("size_value", sa.Float, nullable=True),
        sa.Column("size_unit", sa.Text, nullable=True),
        sa.Column("raw_size", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_product_variants_product_id", "product_variants", ["product_id"])
    op.create_index("idx_product_variants_sku", "product_variants", ["sku"])

    op.execute(
        "CREATE UNIQUE INDEX idx_product_variants_sku_not_null ON product_variants (sku) WHERE sku IS NOT NULL"
    )


def downgrade() -> None:
    op.drop_index("idx_product_variants_sku_not_null", table_name="product_variants")
    op.drop_table("product_variants")
    op.drop_index("idx_products_category", table_name="products")
    op.drop_index("idx_products_name", table_name="products")
    op.drop_index("idx_products_catalog_document_id", table_name="products")
    op.drop_table("products")
    op.drop_index("idx_catalog_documents_imported_at", table_name="catalog_documents")
    op.drop_table("catalog_documents")