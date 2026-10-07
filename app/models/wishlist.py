from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Wishlist(TimestampMixin, Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    customer = relationship("Customer")
    product = relationship("Product")

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "product_id",
            name="uq_customer_product_wishlist"
        ),
    )