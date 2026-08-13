from uuid import UUID

from domain.schemas.product import ProductCreate
from sqlalchemy.orm import Session

from datasource.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ProductCreate) -> Product:
        product = Product(
            name=payload.name,
            category=payload.category,
            price=payload.price,
            available_stock=payload.available_stock,
            supplier_id=payload.supplier_id,
            image_id=payload.image_id if payload.image_id else None,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def decrease_stock(self, product_id: UUID, amount: int):
        if amount <= 0:
            raise ValueError("Amount should be >= 0")
        product = self.get_by_id(product_id)
        if product is None:
            raise ValueError("Product not exist")
        if product.available_stock < amount:
            raise ValueError("Available stock is less than amount")
        product.available_stock -= amount
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: UUID) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def list_available(self, limit: int | None, offset: int | None) -> list[Product]:
        query = self.db.query(Product).filter(Product.available_stock >= 0)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    def delete(self, product_id: UUID) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False
        self.db.delete(product)
        self.db.commit()
        return True
