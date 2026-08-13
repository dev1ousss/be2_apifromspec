from uuid import UUID

from datasource.database import get_db
from datasource.repositories.product_repository import ProductRepository
from domain.schemas.product import ProductCreate, ProductRead
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/product", tags=["product"])


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new product, supplier_id should exist",
)
def create_product(
    payload: ProductCreate, repo: ProductRepository = Depends(get_product_repository)
):
    try:
        return repo.create(payload)
    except IntegrityError:
        repo.db.rollback()
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Supplier with this id not found"
        )


@router.post(
    "/{product_id}/decrease",
    response_model=ProductRead,
    summary="Update product amount",
    description="Posts new amount of available products, decreasing amount should be > 0 and < available in stock",
)
def decrease_stock(
    product_id: UUID,
    amount: int = Query(..., gt=0, description="Decreasing amount"),
    repo: ProductRepository = Depends(get_product_repository),
):
    try:
        product = repo.decrease_stock(product_id, amount)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get("", response_model=list[ProductRead], summary="Get all available products")
def get_available_products(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    repo: ProductRepository = Depends(get_product_repository),
):
    return repo.list_available(limit, offset)


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete product"
)
def delete_product(
    product_id: UUID, repo: ProductRepository = Depends(get_product_repository)
):
    if repo.delete(product_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Get product by id",
)
def get_product(
    product_id: UUID, repo: ProductRepository = Depends(get_product_repository)
):
    product = repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
    return product
