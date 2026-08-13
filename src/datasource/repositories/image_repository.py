from uuid import UUID

from sqlalchemy.orm import Session

from datasource.models.image import Image
from datasource.models.product import Product


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, content: bytes, product_id: UUID) -> Image:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise ValueError("Product not found")

        image = Image(image=content)
        self.db.add(image)
        self.db.flush()

        product.image_id = image.id
        self.db.commit()
        self.db.refresh(image)
        return image

    def update(self, image_id: UUID, content: bytes) -> Image | None:
        image = self.get_by_id(image_id)
        if image is None:
            return None
        image.image = content
        self.db.commit()
        self.db.refresh(image)
        return image

    def delete(self, image_id: UUID) -> bool:
        image = self.get_by_id(image_id)
        product = self.db.query(Product).where(Product.image_id == image_id).first()
        if product is not None:
            product.image_id = None
        self.db.delete(image)
        self.db.commit()
        return True

    def get_by_id(self, image_id: UUID) -> Image | None:
        return self.db.query(Image).where(Image.id == image_id).first()

    def get_by_product_id(self, product_id: UUID) -> Image | None:
        return (
            self.db.query(Image)
            .join(Product, Product.image_id == Image.id)
            .filter(Product.id == product_id)
            .first()
        )
