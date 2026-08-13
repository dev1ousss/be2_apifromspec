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

    def update(self): ...

    def delete(self): ...

    def get_by_id(self): ...

    def get_by_product_id(self): ...
