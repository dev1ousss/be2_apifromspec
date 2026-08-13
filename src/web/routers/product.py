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
