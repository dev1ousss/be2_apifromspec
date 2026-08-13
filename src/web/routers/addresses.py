from uuid import UUID

from datasource.database import get_db
from datasource.repositories.address_repository import AddressRepository
from domain.schemas.address import AddressCreate, AddressRead, AddressUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/addresses", tags=["Address"])


def get_address_repository(db: Session = Depends(get_db)) -> AddressRepository:
    """
    Dependency provider for AddressRepository.
    """
    return AddressRepository(db)


@router.post(
    "",
    response_model=AddressRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="Accepts country, city, and street details, creates a persistent address record in the database, and returns the generated UUID.",
    responses={
        201: {"description": "Address successfully created and persisted."},
        400: {"description": "Invalid JSON payload or validation constraints failed."},
    },
)
def create_address(
    payload: AddressCreate, repo: AddressRepository = Depends(get_address_repository)
):
    return repo.create(payload)


@router.get(
    "/{address_id}",
    response_model=AddressRead,
    summary="Get address by ID",
    description="Retrieves full details of a specific address from the database using its unique UUID identifier.",
    responses={
        200: {"description": "Address successfully retrieved."},
        404: {"description": "Requested address UUID not found in the database."},
    },
)
def get_address(
    address_id: UUID, repo: AddressRepository = Depends(get_address_repository)
):
    address = repo.get_by_id(address_id)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


@router.put(
    "/{address_id}",
    response_model=AddressRead,
    summary="Update an existing address",
    description="Performs a full resource update (replacement) for the specified address ID. All payload fields are required.",
    responses={
        200: {"description": "Address successfully updated and saved."},
        400: {"description": "Validation constraints failed for update payload."},
        404: {"description": "Address with the specified UUID not found."},
    },
)
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


@router.get(
    "",
    response_model=list[AddressRead],
    summary="Get a paginated list of addresses",
    description="Returns a list of all existing addresses using limit and offset pagination. Returns an empty array if no records match.",
    responses={
        200: {
            "description": "Paginated array of address records returned successfully."
        },
    },
)
def list_addresses(
    limit: int | None = None,
    offset: int | None = None,
    repo: AddressRepository = Depends(get_address_repository),
):
    return repo.list_all(limit=limit, offset=offset)


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an address by ID",
    description="Deletes the specified address from the database by its unique UUID. Returns an empty response with HTTP status 204.",
    responses={
        204: {"description": "Address successfully removed. No content returned."},
        404: {"description": "Address with the specified UUID not found."},
    },
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
