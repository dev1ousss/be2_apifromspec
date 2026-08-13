from uuid import UUID

from datasource import ClientRepository
from datasource.database import get_db
from domain.schemas import AddressCreate
from domain.schemas.client import ClientCreate, ClientRead
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_repository(db: Session = Depends(get_db)) -> ClientRepository:
    return ClientRepository(db)


@router.post(
    "",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create client",
    description="Creates a new client with address via one transaction",
)
def create_client(
    payload: ClientCreate, repo: ClientRepository = Depends(get_client_repository)
):
    return repo.create(payload)


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete client",
    description="Deletes client via id, address remains in DB",
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
    summary="Finds clients via name, surname",
)
def search_clients(
    name: str = Query(..., min_length=1, max_length=100, description="Name"),
    surname=Query(..., min_length=1, max_length=100, description="Surname"),
    repo: ClientRepository = Depends(get_client_repository),
):
    return repo.get_by_name_surname(name, surname)


@router.get("", response_model=list[ClientRead], summary="Get all clients")
def list_clients(
    limit: int | None = None,
    offset: int | None = None,
    repo: ClientRepository = Depends(get_client_repository),
):
    return repo.list_all(limit=limit, offset=offset)


@router.put(
    "/{client_id}/address",
    response_model=ClientRead,
    summary="Change client's address",
    description="Updates client's address",
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
