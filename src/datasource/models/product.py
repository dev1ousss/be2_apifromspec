import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from datasource.database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    category: Mapped[str] = mapped_column(String(100), nullable=False)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)

    available_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    last_update_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),    
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("supplier.id", ondelete="RESTRICT"),
        nullable=False,
    )

    image_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("images.id", ondelete="SET NULL"), nullable=True
    )
