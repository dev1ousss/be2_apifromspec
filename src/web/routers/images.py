from uuid import UUID

from datasource.database import get_db
from datasource.repositories.image_repository import ImageRepository
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
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


@router.put(
    "/{image_id}",
    summary="Change the image",
    description="Changes the image by its' id",
)
def update_image(
    image_id: UUID,
    file: UploadFile = File(..., description="New image file"),
    repo: ImageRepository = Depends(get_images_repository),
):
    content = file.file.read()
    image = repo.update(image_id, content)
    if image is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Image not found")
    return {"image_id": image.id}


@router.get("/{image_id}", summary="Get image by its' id")
def get_image(image_id: UUID, repo: ImageRepository = Depends(get_images_repository)):
    image = repo.get_by_id(image_id)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found")
    return Response(
        content=image.image,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename=image_{image.id}.bin"},
    )


@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete image by its' id",
)
def delete_image(
    image_id: UUID, repo: ImageRepository = Depends(get_images_repository)
):
    if not repo.delete(image_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found")
    return None


@router.get("/product/{product_id}", summary="Get product image by product id")
def get_image_by_product_id(
    product_id: UUID, repo: ImageRepository = Depends(get_images_repository)
):
    image = repo.get_by_product_id(product_id)

    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found")
    return Response(
        content=image.image,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename=image_{image.id}.bin"},
    )
