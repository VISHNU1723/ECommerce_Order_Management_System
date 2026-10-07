from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Cart(TimestampMixin, Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        unique=True
    )

    customer = relationship(
        "Customer",
        back_populates="cart"
    )

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


class CartItem(TimestampMixin, Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    cart_id = Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    cart = relationship(
        "Cart",
        back_populates="items"
    )

    product = relationship(
        "Product",
        back_populates="cart_items"
    )

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="uq_cart_product"
        ),
    )