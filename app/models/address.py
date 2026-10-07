from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Address(TimestampMixin, Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(10),
        nullable=False
    )

    address_line = Column(
        String(255),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    state = Column(
        String(100),
        nullable=False
    )

    pincode = Column(
        String(6),
        nullable=False
    )

    is_default = Column(
        Boolean,
        nullable=False,
        default=False
    )

    customer = relationship(
        "Customer",
        back_populates="addresses"
    )

    orders = relationship(
        "Order",
        back_populates="address"
    )