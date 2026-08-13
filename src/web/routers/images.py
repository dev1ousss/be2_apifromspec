from uuid import UUID

from datasource.database import get_db
from datasource.repositories.image_repository import ImageRepository
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/images", tags=["images"])


def get_images_repository(db: Session = Depends(get_db)):
    return ImageRepository(db)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Add new image to product",
    description="Add new image to the product using product id",
)
def upload_image(
    product_id: UUID,
    file: UploadFile = File(..., description="Image file"),
    repo: ImageRepository = Depends(get_images_repository),
):
    content = file.file.read()
    try:
        image = repo.create(content, product_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return {"image_id": image.id}
