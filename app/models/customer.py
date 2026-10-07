from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Customer(TimestampMixin, Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False,
        default="customer"
    )

    cart = relationship(
        "Cart",
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan"
    )

    addresses = relationship(
        "Address",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    orders = relationship(
        "Order",
        back_populates="customer"
    )

    reviews = relationship(
        "Review",
        back_populates="customer"
    )

    returns = relationship(
        "ReturnRequest",
        back_populates="customer"
    )