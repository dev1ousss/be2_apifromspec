from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "OnePlus 8 Pro",
                "category": "Mobile",
                "price": 30000.01,
                "available_stock": 5,
                "supplier_id": "c048a5af-3bf0-42f5-8702-d4a60f6f09ca",
                "image_id": None,
            }
        }
    )
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    category: str = Field(
        ..., min_length=1, max_length=100, description="Product category"
    )
    price: float = Field(..., gt=0, description="Product price (>0)")
    available_stock: int = Field(
        ..., ge=0, description="Product available in stock (>=0)"
    )
    supplier_id: UUID = Field(..., description="Product supplier id")
    image_id: UUID | None = Field(None, description="Product image id (optional)")


class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    category: str = Field(
        ..., min_length=1, max_length=100, description="Product category"
    )
    price: float = Field(..., gt=0, description="Product price (>0)")
    available_stock: int = Field(
        ..., ge=0, description="Product available in stock (>=0)"
    )


class ProductPatch(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    available_stock: int | None = None


class ProductRead(BaseModel):
    id: UUID = Field(..., description="Product ID")
    name: str
    category: str
    price: float
    available_stock: int
    last_update_date: datetime
    supplier_id: UUID = Field(..., description="Product supplier id")
    image_id: UUID | None = Field(None, description="Product image id (optional)")

    class Config:
        from_attributes = True
