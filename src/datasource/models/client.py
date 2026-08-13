import uuid
from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, relationships

from datasource.database import Base
from datasource.models.address import Address


class Client(Base):
    __tablename__ = "client"

    __table_args__ = (CheckConstraint("gender IN ('M', 'F')", name="check_gender"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_name: Mapped[str] = mapped_column(String(100), nullable=False)
    client_surname: Mapped[str] = mapped_column(String(100), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("address.id", ondelete="RESTRICT"),
        nullable=False,
    )
    address: Mapped["Address"] = relationship(lazy="joined")
