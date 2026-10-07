from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Payment(TimestampMixin, Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_method = Column(
        String(30),
        nullable=False
    )

    transaction_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    status = Column(
        String(20),
        nullable=False
    )

    order = relationship(
        "Order",
        back_populates="payments"
    )