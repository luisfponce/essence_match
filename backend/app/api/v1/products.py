from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_session
from app.models.catalog import Product, ProductVariant
from app.schemas.catalog import ProductRead


router = APIRouter(tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    category: str | None = Query(default=None, pattern="^(essential_oil|essential_oil_blend|plus_flavoring|other)$"),
    name: str | None = Query(default=None),
    sku: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> list[ProductRead]:
    query = session.query(Product)

    if category:
        query = query.filter(Product.category == category)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if sku:
        query = query.join(ProductVariant).filter(ProductVariant.sku == sku)

    products = query.distinct().all()
    return products


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)) -> ProductRead:
    product = session.query(Product).options(selectinload(Product.variants)).get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
