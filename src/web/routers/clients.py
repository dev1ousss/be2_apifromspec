from uuid import UUID

from datasource import ClientRepository
from datasource.database import get_db
from domain.schemas import AddressCreate
from domain.schemas.client import ClientCreate, ClientRead
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_repository(db: Session = Depends(get_db)) -> ClientRepository:
    """
    Dependency provider for ClientRepository.
    """
    return ClientRepository(db)


@router.post(
    "",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new client",
    description="Creates a new client record along with their address in a single transactional operation.",
    responses={
        201: {"description": "Client and their address successfully created."},
        400: {
            "description": "Invalid payload data, gender constraint violation, or duplicate fields."
        },
    },
)
def create_client(
    payload: ClientCreate, repo: ClientRepository = Depends(get_client_repository)
):
    return repo.create(payload)


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a client by ID",
    description="Removes the client record from the database by its unique UUID. The linked address record remains untouched.",
    responses={
        204: {"description": "Client successfully removed. No content returned."},
        404: {"description": "Client with the specified UUID not found."},
    },
)
def delete_client(
    client_id: UUID, repo: ClientRepository = Depends(get_client_repository)
):
    if not repo.delete(client_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return None


@router.get(
    "/search",
    response_model=list[ClientRead],
    summary="Search clients by name and surname",
    description="Retrieves a list of clients matching both the provided name and surname filters.",
    responses={
        200: {"description": "Array of matching client records successfully returned."},
        400: {
            "description": "Missing required query parameters or constraints failed."
        },
    },
)
def search_clients(
    name: str = Query(..., min_length=1, max_length=100, description="Name"),
    surname=Query(..., min_length=1, max_length=100, description="Surname"),
    repo: ClientRepository = Depends(get_client_repository),
):
    return repo.get_by_name_surname(name, surname)


@router.get(
    "",
    response_model=list[ClientRead],
    summary="Get a paginated list of clients",
    description="Returns an array of existing clients using offset-based pagination. Returns an empty array if no clients match.",
    responses={
        200: {
            "description": "Paginated array of client records returned successfully."
        },
    },
)
def list_clients(
    limit: int | None = None,
    offset: int | None = None,
    repo: ClientRepository = Depends(get_client_repository),
):
    return repo.list_all(limit=limit, offset=offset)


@router.put(
    "/{client_id}/address",
    response_model=ClientRead,
    summary="Update client's address",
    description="Modifies the existing address details associated with the specified client ID.",
    responses={
        200: {"description": "Client's address details successfully updated."},
        400: {"description": "Validation constraints failed for address payload."},
        404: {"description": "Client with the specified UUID not found."},
    },
)
def update_client_address(
    client_id: UUID,
    payload: AddressCreate,
    repo: ClientRepository = Depends(get_client_repository),
):
    client = repo.update_address(client_id, payload)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client
