from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Category(TimestampMixin, Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    products = relationship(
        "Product",
        back_populates="category"
    )