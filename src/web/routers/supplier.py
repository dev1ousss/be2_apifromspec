from uuid import UUID

from datasource.database import get_db
from datasource.repositories.supplier_repository import SupplierRepository
from domain.schemas import AddressCreate
from domain.schemas.supplier import SupplierCreate, SupplierRead
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/supplier", tags=["supplier"])


def get_supplier_repository(db: Session = Depends(get_db)) -> SupplierRepository:
    return SupplierRepository(db)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create new supplier")
def create_supplier(
    payload: SupplierCreate,
    repo: get_supplier_repository = Depends(get_supplier_repository),
):
    return repo.create(payload)


@router.get("", response_model=list[SupplierRead], summary="Get all suppliers")
def list_suppliers(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    repo: SupplierRepository = Depends(get_supplier_repository),
):
    return repo.list_all(limit, offset)


@router.patch(
    "{supplier_id}/address",
    response_model=SupplierRead,
    summary="Update supplier's address",
)
def update_supplier_address(
    supplier_id: UUID,
    payload: AddressCreate,
    repo: SupplierRepository = Depends(get_supplier_repository),
):
    supplier = repo.update_address(supplier_id, payload)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.delete(
    "/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete supplier"
)
def delete_supplier(
    supplier_id: UUID, repo: SupplierRepository = Depends(get_supplier_repository)
):
    if not repo.delete(supplier_id):
        raise HTTPException(status_code=404, detail="Supplier not found")
    return None


@router.get("/{supplier_id}", response_model=SupplierRead, summary="Get supplier by id")
def get_supplier(
    supplier_id: UUID, repo: SupplierRepository = Depends(get_supplier_repository)
):
    supplier = repo.get_by_id(supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier
