from uuid import UUID

from domain.schemas.address import AddressCreate
from domain.schemas.supplier import SupplierCreate
from sqlalchemy.orm import Session

from datasource.models.address import Address
from datasource.models.supplier import Supplier


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: SupplierCreate) -> Supplier:
        address = Address(
            country=payload.address.country,
            city=payload.address.city,
            street=payload.address.street,
        )
        self.db.add(address)
        self.db.flush()

        supplier = Supplier(
            name=payload.name,
            phone_number=payload.phone_number,
            address_id=address.id,
        )
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)

    def get_by_id(self, supplier_id: UUID) -> Supplier | None:
        return self.db.query(Supplier).where(Supplier.id == supplier_id).first()

    def update_address(
        self, supplier_id: UUID, payload: AddressCreate
    ) -> Supplier | None:
        supplier = self.get_by_id(supplier_id)
        if supplier is None:
            return None
        supplier.address.country = payload.country
        supplier.address.city = payload.city
        supplier.address.street = payload.street
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def delete(self, supplier_id: UUID) -> bool:
        supplier = self.get_by_id(supplier_id)
        if supplier is None:
            return False
        self.db.delete(supplier)
        self.db.commit()
        return True

    def list_all(self, limit: int | None, offset: int | None) -> list[Supplier]:
        query = self.db.query(Supplier)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(limit)
        return query.all()
