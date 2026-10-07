from sqlalchemy import (
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


class ReturnRequest(TimestampMixin, Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    reason = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="Requested"
    )

    refund_amount = Column(
        Numeric(10, 2),
        nullable=True
    )

    rejection_reason = Column(
        Text,
        nullable=True
    )

    order = relationship(
        "Order",
        back_populates="return_request"
    )

    customer = relationship(
        "Customer",
        back_populates="returns"
    )