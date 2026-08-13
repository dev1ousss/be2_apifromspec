from uuid import UUID

from datasource.database import get_db
from datasource.repositories.address_repository import AddressRepository
from domain.schemas.address import AddressCreate, AddressRead, AddressUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/addresses", tags=["Address"])


def get_address_repository(db: Session = Depends(get_db)) -> AddressRepository:
    return AddressRepository(db)


@router.post(
    "",
    response_model=AddressRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create address",
)
def create_address(
    payload: AddressCreate, repo: AddressRepository = Depends(get_address_repository)
):
    return repo.create(payload)


@router.get("/{address_id}", response_model=AddressRead, summary="Get address by id")
def get_address(
    address_id: UUID, repo: AddressRepository = Depends(get_address_repository)
):
    address = repo.get_by_id(address_id)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


@router.put("/{address_id}", response_model=AddressRead, summary="Update address")
def update_address(
    address_id: UUID,
    payload: AddressUpdate,
    repo: AddressRepository = Depends(get_address_repository),
):
    address = repo.update(address_id, payload)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


@router.get("", response_model=list[AddressRead], summary="Get all addresses")
def list_addresses(
    limit: int | None = None,
    offset: int | None = None,
    repo: AddressRepository = Depends(get_address_repository),
):
    return repo.list_all(limit=limit, offset=offset)


@router.delete(
    "/{address_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete address"
)
def delete_address(
    address_id: UUID, repo: AddressRepository = Depends(get_address_repository)
):
    deleted = repo.delete(address_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return None
