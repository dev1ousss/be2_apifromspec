from uuid import UUID

from pydantic import BaseModel, Field


class ImageCreate(BaseModel):
    images: bytes = Field(..., description="Image in bytes")


class ImageUpdate(BaseModel):
    images: bytes = Field(..., description="Image in bytes")


class ImageRead(BaseModel):
    id: UUID = Field(..., description="Image id")
    images: bytes

    class Config:
        from_attributes = True
