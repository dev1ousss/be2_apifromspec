from uuid import UUID

from domain.schemas import AddressCreate
from domain.schemas.client import ClientCreate
from sqlalchemy.orm import Session

from datasource.models.address import Address
from datasource.models.client import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ClientCreate) -> Client:
        address = Address(
            country=payload.address.country,
            city=payload.address.city,
            street=payload.address.street,
        )
        self.db.add(address)
        self.db.flush()
        client = Client(
            client_name=payload.client_name,
            client_surname=payload.client_surname,
            birthday=payload.birthday,
            gender=payload.gender,
            address_id=address.id,
        )
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_by_id(self, client_id: UUID) -> Client | None:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def delete(self, client_id: UUID) -> bool:
        client = self.get_by_id(client_id)
        if client is None:
            return False
        self.db.delete(client)
        self.db.commit()
        return True

    def get_by_name_surname(self, name: str, surname: str) -> list[Client]:
        return (
            self.db.query(Client)
            .filter(Client.client_name == name, Client.client_surname == surname)
            .all()
        )

    def update_address(self, client_id: UUID, payload: AddressCreate) -> Client:
        client = self.get_by_id(client_id)
        if client is None:
            return None
        client.address.country = payload.country
        client.address.city = payload.city
        client.address.street = payload.street
        self.db.commit()
        self.db.refresh(client)
        return client

    def list_all(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Client]:
        query = self.db.query(Client)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(limit)
        return query.all()
