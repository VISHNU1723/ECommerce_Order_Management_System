from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Review(TimestampMixin, Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    rating = Column(
        Integer,
        nullable=False
    )

    comment = Column(
        Text,
        nullable=True
    )

    product = relationship(
        "Product",
        back_populates="reviews"
    )

    customer = relationship(
        "Customer",
        back_populates="reviews"
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "customer_id",
            name="uq_product_customer_review"
        ),
    )