import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.catalog.importer import CatalogImportService, import_from_file
from app.models.catalog import CatalogDocument, Product, ProductVariant
from app.schemas.catalog import ProductRead, ProductVariantRead


SAMPLE_CATALOG = {
    "source_pdf": "synthetic_catalog.pdf",
    "extraction_version": "0.1.0",
    "metadata": {"fixture": "synthetic"},
    "products": [
        {
            "name": "Lavender",
            "scientific_name": "Lavandula angustifolia",
            "category": "essential_oil",
            "description": "A gentle floral essence often chosen for calm routines and evening wind-downs.",
            "ingredients": ["Lavandula angustifolia"],
            "usage_text": "Diffuse during quiet time or add to a bedtime aroma routine.",
            "usage_modes": ["aromatic", "topical"],
            "variants": [
                {"sku": "358011", "size_value": 5.0, "size_unit": "ml", "raw_size": "5 ml"},
                {"sku": "357511", "size_value": 15.0, "size_unit": "ml", "raw_size": "15 ml"},
            ],
            "seasonal": False,
            "image": {
                "path": "images/lavender.webp",
                "format": "webp",
                "source_page": 9,
                "source_xref": 1,
                "bbox": [10.0, 20.0, 100.0, 200.0],
                "sha256": "abc123",
            },
            "source": {"document_name": "synthetic_catalog.pdf", "page": 9, "card_bbox": [40.0, 90.0, 297.5, 265.1]},
            "raw_text": "LAVENDER\nSKU SIZE\n358011 5 ml\n357511 15 ml",
            "extraction_confidence": 0.95,
            "warnings": [],
            "derived_tags": ["calm", "sleep"],
        },
        {
            "name": "Peppermint",
            "scientific_name": None,
            "category": "essential_oil",
            "description": "A bright, cooling essence.",
            "ingredients": ["Mentha piperita"],
            "usage_text": "Diffuse for an alert workspace.",
            "usage_modes": ["aromatic"],
            "variants": [{"sku": "350011", "size_value": 15.0, "size_unit": "ml", "raw_size": "15 ml"}],
            "seasonal": False,
            "image": None,
            "source": {"document_name": "synthetic_catalog.pdf", "page": 15, "card_bbox": None},
            "raw_text": "PEPPERMINT\nSKU SIZE\n350011 15 ml",
            "extraction_confidence": 0.9,
            "warnings": ["low_confidence"],
            "derived_tags": [],
        },
        {
            "name": "Lemon",
            "scientific_name": None,
            "category": "plus_flavoring",
            "description": None,
            "ingredients": [],
            "usage_text": None,
            "usage_modes": [],
            "variants": [],
            "seasonal": True,
            "image": None,
            "source": {"document_name": "synthetic_catalog.pdf", "page": 25, "card_bbox": None},
            "raw_text": "LEMON\n",
            "extraction_confidence": 0.8,
            "warnings": ["description_identity_mismatch"],
            "derived_tags": ["citrus"],
        },
    ],
}


def test_catalog_document_creation(session: Session) -> None:
    doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="abc123",
        extraction_version="0.1.0",
        metadata={"test": True},
        raw_payload=None,
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)

    assert doc.id is not None
    assert doc.source_pdf == "test.pdf"
    assert doc.source_hash == "abc123"
    assert doc.extraction_version == "0.1.0"
    assert doc.metadata == {"test": True}
    assert doc.raw_payload is None
    assert doc.imported_at is not None


def test_product_creation(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Test Product",
        scientific_name="Scientific Name",
        category="essential_oil",
        description="A test product",
        ingredients=["ingredient1", "ingredient2"],
        usage_text="Use as directed",
        usage_modes=["aromatic"],
        seasonal=False,
        image_metadata={"path": "image.webp"},
        source_document_name="test.pdf",
        source_page=1,
        source_card_bbox=[0.0, 0.0, 100.0, 100.0],
        raw_text="RAW TEXT",
        extraction_confidence=0.95,
        warnings=["warning1"],
        derived_tags=["tag1"],
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.id is not None
    assert product.name == "Test Product"
    assert product.catalog_document_id == catalog_doc.id
    assert product.ingredients == ["ingredient1", "ingredient2"]
    assert product.usage_modes == ["aromatic"]
    assert product.warnings == ["warning1"]
    assert product.derived_tags == ["tag1"]
    assert product.created_at is not None
    assert product.updated_at is not None


def test_product_with_zero_variants(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="No Variants Product",
        ingredients=[],
        usage_modes=[],
        warnings=[],
        derived_tags=[],
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert len(product.variants) == 0


def test_product_with_one_variant(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="One Variant Product",
    )
    session.add(product)
    session.flush()

    variant = ProductVariant(
        product_id=product.id,
        sku="SKU001",
        size_value=10.0,
        size_unit="ml",
        raw_size="10 ml",
    )
    session.add(variant)
    session.commit()
    session.refresh(product)

    assert len(product.variants) == 1
    assert product.variants[0].sku == "SKU001"


def test_product_with_multiple_variants(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Multi Variant Product",
    )
    session.add(product)
    session.flush()

    variant1 = ProductVariant(product_id=product.id, sku="SKU001", size_value=5.0, size_unit="ml")
    variant2 = ProductVariant(product_id=product.id, sku="SKU002", size_value=15.0, size_unit="ml")
    session.add_all([variant1, variant2])
    session.commit()
    session.refresh(product)

    assert len(product.variants) == 2
    skus = {v.sku for v in product.variants}
    assert skus == {"SKU001", "SKU002"}


def test_nullable_scientific_name(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="No Scientific Name",
        scientific_name=None,
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.scientific_name is None


def test_empty_ingredients(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Empty Ingredients",
        ingredients=[],
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.ingredients == []


def test_empty_usage_modes(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Empty Usage Modes",
        usage_modes=[],
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.usage_modes == []


def test_nullable_image_metadata(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="No Image",
        image_metadata=None,
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.image_metadata is None


def test_source_provenance(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Provenance Test",
        source_document_name="test.pdf",
        source_page=42,
        source_card_bbox=[1.0, 2.0, 3.0, 4.0],
        raw_text="RAW TEXT HERE",
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.source_document_name == "test.pdf"
    assert product.source_page == 42
    assert product.source_card_bbox == [1.0, 2.0, 3.0, 4.0]
    assert product.raw_text == "RAW TEXT HERE"


def test_extraction_confidence(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Confidence Test",
        extraction_confidence=0.87,
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.extraction_confidence == 0.87


def test_warnings_jsonb(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Warnings Test",
        warnings=["low_confidence", "variant_parse_failed"],
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.warnings == ["low_confidence", "variant_parse_failed"]


def test_derived_tags_jsonb(session: Session) -> None:
    catalog_doc = CatalogDocument(
        source_pdf="test.pdf",
        source_hash="hash123",
        extraction_version="0.1.0",
        metadata={},
        raw_payload=None,
    )
    session.add(catalog_doc)
    session.commit()
    session.refresh(catalog_doc)

    product = Product(
        catalog_document_id=catalog_doc.id,
        name="Tags Test",
        derived_tags=["citrus", "uplifting"],
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.derived_tags == ["citrus", "uplifting"]


def test_catalog_import_transaction(session: Session) -> None:
    service = CatalogImportService(session)

    result = service.import_document(SAMPLE_CATALOG)

    assert result["status"] == "imported"
    assert result["catalog_document_id"] is not None
    assert result["products"] == 3
    assert result["variants"] == 3
    assert result["warnings"] == 2

    docs = session.query(CatalogDocument).all()
    assert len(docs) == 1

    products = session.query(Product).all()
    assert len(products) == 3

    variants = session.query(ProductVariant).all()
    assert len(variants) == 3


def test_repeated_import_does_not_duplicate(session: Session) -> None:
    service = CatalogImportService(session)

    result1 = service.import_document(SAMPLE_CATALOG)
    assert result1["status"] == "imported"
    doc_id = result1["catalog_document_id"]

    result2 = service.import_document(SAMPLE_CATALOG)
    assert result2["status"] == "already_imported"
    assert result2["catalog_document_id"] == doc_id

    docs = session.query(CatalogDocument).all()
    assert len(docs) == 1

    products = session.query(Product).all()
    assert len(products) == 3


def test_get_products_endpoint(client, session: Session) -> None:
    service = CatalogImportService(session)
    service.import_document(SAMPLE_CATALOG)

    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_products_filter_by_category(client, session: Session) -> None:
    service = CatalogImportService(session)
    service.import_document(SAMPLE_CATALOG)

    response = client.get("/api/v1/products?category=essential_oil")
    assert response.status_code == 200
    data = response.json()
    assert all(p["category"] == "essential_oil" for p in data)


def test_get_products_filter_by_name(client, session: Session) -> None:
    service = CatalogImportService(session)
    service.import_document(SAMPLE_CATALOG)

    response = client.get("/api/v1/products?name=Lavender")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Lavender"


def test_get_products_filter_by_sku(client, session: Session) -> None:
    service = CatalogImportService(session)
    service.import_document(SAMPLE_CATALOG)

    response = client.get("/api/v1/products?sku=358011")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Lavender"
    assert any(v["sku"] == "358011" for v in data[0]["variants"])


def test_get_product_by_id(client, session: Session) -> None:
    service = CatalogImportService(session)
    service.import_document(SAMPLE_CATALOG)

    product = session.query(Product).filter(Product.name == "Lavender").first()
    assert product is not None

    response = client.get(f"/api/v1/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product.id
    assert data["name"] == "Lavender"
    assert len(data["variants"]) == 2
    variant_skus = {v["sku"] for v in data["variants"]}
    assert variant_skus == {"358011", "357511"}


def test_get_product_not_found(client) -> None:
    response = client.get("/api/v1/products/999999")
    assert response.status_code == 404


def test_catalog_import_cli(tmp_path: Path) -> None:
    catalog_file = tmp_path / "catalog.json"
    catalog_file.write_text(json.dumps(SAMPLE_CATALOG))

    result = import_from_file(catalog_file)

    assert result["status"] == "imported"
    assert result["products"] == 3
    assert result["variants"] == 3


def test_product_read_schema_includes_variants(session: Session) -> None:
    service = CatalogImportService(session)
    service.import_document(SAMPLE_CATALOG)

    product = session.query(Product).filter(Product.name == "Lavender").first()
    assert product is not None

    read_model = ProductRead.model_validate(product)
    assert len(read_model.variants) == 2
    assert isinstance(read_model.variants[0], ProductVariantRead)
    assert read_model.variants[0].sku == "358011"
    assert read_model.variants[1].sku == "357511"