from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from app.database import Base
from app.models.base import TimestampMixin


class Coupon(TimestampMixin, Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_type = Column(String(20), nullable=False)  # percentage / flat
    discount_value = Column(Numeric(10, 2), nullable=False)
    minimum_order_value = Column(Numeric(10, 2), nullable=False, default=0)
    expiry_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=False)
    used_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)