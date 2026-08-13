from datetime import date
from uuid import UUID

from domain.schemas import AddressCreate, AddressRead
from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_name": "Ivan",
                "client_surname": "Shurpatov",
                "birthday": "1991-09-11",
                "gender": "M",
                "address": {
                    "country": "Russia",
                    "city": "Moscow",
                    "street": "Tverskaya 52",
                },
            }
        }
    )
    client_name: str = Field(
        ..., min_length=1, max_length=100, description="Client name"
    )
    client_surname: str = Field(
        ..., min_length=1, max_length=100, description="Client surname"
    )
    birthday: str = Field(
        ..., min_length=1, max_length=100, description="Date of birth (yyyy-mm-dd"
    )
    gender: str = Field(..., pattern=r"^[MF]$", description="Gender (M or F)")
    address: AddressCreate


class ClientUpdate(ClientCreate):
    client_name: str = Field(..., min_length=1, max_length=100, description="Name")
    client_surname: str = Field(
        ..., min_length=1, max_length=100, description="Surname"
    )
    birthday: date = Field(..., description="Date of birth (yyyy-mm-dd")
    gender: str = Field(
        ..., min_length=1, max_length=100, description="Gender (M or F)"
    )


class ClientPatch(BaseModel):
    client_name: str | None = None
    client_surname: str | None = None
    birthday: date | None = None
    gender: str | None = None


class ClientRead(BaseModel):
    id: UUID = Field(..., description="Client id")
    client_name: str
    client_surname: str
    birthday: date
    gender: str
    address: AddressRead

    class Config:
        from_attributes = True
