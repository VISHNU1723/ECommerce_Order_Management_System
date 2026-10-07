from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    order_number = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    address_id = Column(
        Integer,
        ForeignKey("addresses.id"),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    tax_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    delivery_charge = Column(
        Numeric(10, 2),
        nullable=False
    )

    grand_total = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="Pending"
    )

    payment_status = Column(
        String(20),
        nullable=False,
        default="Unpaid"
    )

    delivered_at = Column(
        DateTime,
        nullable=True
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    address = relationship(
        "Address",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    return_request = relationship(
        "ReturnRequest",
        back_populates="order",
        uselist=False
    )


class OrderItem(TimestampMixin, Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    line_total = Column(
        Numeric(10, 2),
        nullable=False
    )

    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )