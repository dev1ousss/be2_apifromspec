from uuid import UUID

from domain.schemas.address import AddressCreate, AddressUpdate
from sqlalchemy.orm import Session

from datasource.models.address import Address


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: AddressCreate):
        address = Address(
            country=payload.country, city=payload.city, street=payload.street
        )
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_by_id(self, address_id: UUID) -> Address | None:
        return self.db.query(Address).filter(Address.id == address_id).first()

    def update(self, address_id: UUID, payload: AddressUpdate):
        address = self.get_by_id(address_id)
        if address is None:
            return None
        address.country = payload.country
        address.city = payload.city
        address.street = payload.street
        self.db.commit()
        self.db.refresh(address)
        return address

    def list_all(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Address]:
        query = self.db.query(Address)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return query.all()

    def delete(self, address_id: UUID) -> bool:
        address = self.get_by_id(address_id)
        if address is None:
            return False
        self.db.delete(address)
        self.db.commit()
        return True
