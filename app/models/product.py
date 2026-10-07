from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    sku = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    price = Column(
        Numeric(10, 2),
        nullable=False
    )

    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    reviews = relationship(
        "Review",
        back_populates="product"
    )