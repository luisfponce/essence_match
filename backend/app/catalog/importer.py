import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, init_db
from app.models.catalog import CatalogDocument, Product, ProductVariant


class SourceRefImport(BaseModel):
    document_name: str
    page: int
    card_bbox: list[float] | None = None


class ProductImageImport(BaseModel):
    path: str
    format: str = "webp"
    source_page: int
    source_xref: int | None = None
    bbox: list[float] | None = None
    sha256: str | None = None


class ProductVariantImport(BaseModel):
    sku: str
    size_value: float | None = None
    size_unit: str | None = None
    raw_size: str | None = None


class ProductImport(BaseModel):
    name: str = Field(min_length=1)
    scientific_name: str | None = None
    category: Literal["essential_oil", "essential_oil_blend", "plus_flavoring", "other"] | None = None
    description: str | None = None
    ingredients: list[str] = Field(default_factory=list)
    usage_text: str | None = None
    usage_modes: list[Literal["aromatic", "topical", "dilute", "flavoring", "photosensitive"]] = Field(default_factory=list)
    variants: list[ProductVariantImport] = Field(default_factory=list)
    seasonal: bool = False
    image: ProductImageImport | None = None
    source: SourceRefImport = Field(...)
    raw_text: str
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    warnings: list[str] = Field(default_factory=list)
    derived_tags: list[str] = Field(default_factory=list)


class CatalogDocumentImport(BaseModel):
    source_pdf: str
    products: list[ProductImport]
    extraction_version: str = "0.1.0"
    doc_metadata: dict[str, Any] = Field(default_factory=dict)


class CatalogImportService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def import_document(self, doc: dict[str, Any]) -> dict[str, Any]:
        validated = CatalogDocumentImport.model_validate(doc)
        source_hash = self._compute_hash(json.dumps(validated.model_dump(mode="json"), sort_keys=True).encode("utf-8"))

        try:
            with self.session.begin():
                existing = self.session.query(CatalogDocument).filter_by(source_hash=source_hash).first()
                if existing is not None:
                    return {
                        "status": "already_imported",
                        "catalog_document_id": existing.id,
                        "source_hash": source_hash,
                        "source_pdf": existing.source_pdf,
                        "extraction_version": existing.extraction_version,
                        "products": 0,
                        "variants": 0,
                        "warnings": 0,
                    }

                return self._import_validated(validated, source_hash)
        except Exception:
            self.session.rollback()
            raise

    def _import_validated(self, validated: CatalogDocumentImport, source_hash: str) -> dict[str, Any]:
        catalog_doc = CatalogDocument(
            source_pdf=validated.source_pdf,
            source_hash=source_hash,
            extraction_version=validated.extraction_version,
            doc_metadata=validated.doc_metadata,
            raw_payload=validated.model_dump(mode="json"),
            imported_at=datetime.now(UTC),
        )
        self.session.add(catalog_doc)
        self.session.flush()

        warnings: list[str] = []
        variant_count = 0
        products_count = 0

        for product_raw in validated.products:
            product = self._build_product(catalog_doc.id, product_raw)
            self.session.add(product)
            self.session.flush()

            for variant_raw in product_raw.variants:
                variant = ProductVariant(
                    product_id=product.id,
                    sku=variant_raw.sku,
                    size_value=variant_raw.size_value,
                    size_unit=variant_raw.size_unit,
                    raw_size=variant_raw.raw_size,
                    created_at=datetime.now(UTC),
                )
                self.session.add(variant)
                variant_count += 1

            warnings.extend(product_raw.warnings)
            products_count += 1

        return {
            "status": "imported",
            "catalog_document_id": catalog_doc.id,
            "source_hash": source_hash,
            "source_pdf": catalog_doc.source_pdf,
            "extraction_version": catalog_doc.extraction_version,
            "products": products_count,
            "variants": variant_count,
            "warnings": len(warnings),
        }

    def _build_product(self, catalog_doc_id: int, data: ProductImport) -> Product:
        source = data.source
        image = data.image
        return Product(
            catalog_document_id=catalog_doc_id,
            name=data.name,
            scientific_name=data.scientific_name,
            category=data.category,
            description=data.description,
            ingredients=data.ingredients,
            usage_text=data.usage_text,
            usage_modes=data.usage_modes,
            seasonal=data.seasonal,
            image_metadata=image.model_dump(mode="json") if image is not None else None,
            source_document_name=source.document_name,
            source_page=source.page,
            source_card_bbox=source.card_bbox,
            raw_text=data.raw_text,
            extraction_confidence=data.extraction_confidence,
            warnings=data.warnings,
            derived_tags=data.derived_tags,
        )

    @staticmethod
    def _compute_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()


def import_from_file(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    init_db()
    service = CatalogImportService(session=SessionLocal())
    return service.import_document(data)


def print_import_report(result: dict[str, Any]) -> None:
    status = result.get("status", "unknown")
    print(f"Catalog:\n  {result.get('source_pdf', '')}")
    print(f"\nExtraction version:\n  {result.get('extraction_version', '0.1.0')}")
    print(f"\nProducts:\n  {result.get('products', 0)}")
    print(f"\nVariants:\n  {result.get('variants', 0)}")
    print(f"\nWarnings:\n  {result.get('warnings', 0)}")
    print(f"\nStatus:\n  {status}")
    if status == "already_imported":
        print(f"\nCatalog document ID:\n  {result.get('catalog_document_id')}")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python -m app.catalog.importer /path/to/catalog.json", file=sys.stderr)
        return 2

    path = Path(args[0])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    try:
        result = import_from_file(path)
    except Exception as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        return 1

    print_import_report(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
