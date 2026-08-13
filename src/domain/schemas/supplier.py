from uuid import UUID

from domain.schemas.address import AddressCreate, AddressRead
from pydantic import BaseModel, ConfigDict, Field


class SupplierCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "OOO Techno",
                "phone_number": "+79225263141",
                "address": {
                    "country": "Russia",
                    "city": "Moscow",
                    "street": "Bolshaya Krasnaya 55",
                },
            }
        }
    )
    name: str = Field(..., min_length=1, max_length=100, description="Supplier name")
    phone_number: str = Field(
        ..., min_length=1, max_length=100, description="Supplier phone number"
    )
    address: AddressCreate


class SupplierUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Supplier name")
    phone_number: str = Field(
        ..., min_length=1, max_length=100, description="Supplier phone number"
    )


class SupplierPatch(BaseModel):
    name: str | None = None
    phone_number: str | None = None


class SupplierRead(BaseModel):
    id: UUID = Field(..., description="Supplier ID")
    name: str
    phone_number: str
    address: AddressRead
