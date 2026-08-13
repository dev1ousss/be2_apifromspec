import uuid

from datasource import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .address import Address


class Supplier(Base):
    __tablename__ = "supplier"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("address.id", ondelete="RESTRICT"),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    address: Mapped["Address"] = relationship(lazy="joined")
