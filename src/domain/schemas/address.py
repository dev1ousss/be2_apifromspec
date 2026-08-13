from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "country": "Canada",
                "city": "Toronto",
                "street": "Wall street",
            }
        }
    )
    country: str = Field(..., min_length=1, max_length=100, description="Country")
    city: str = Field(..., min_length=1, max_length=100, description="City")
    street: str = Field(..., min_length=1, max_length=100, description="Street")


class AddressRead(BaseModel):
    id: UUID = Field(..., description="Address id")
    country: str
    city: str
    street: str


class AddressUpdate(AddressCreate):
    pass


class AddressPatch(BaseModel):
    country: str | None = None
    city: str | None = None
    street: str | None = None
