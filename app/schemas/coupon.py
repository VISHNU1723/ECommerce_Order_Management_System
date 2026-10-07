from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class CouponCreate(BaseModel):
    code: str
    discount_type: str
    discount_value: Decimal = Field(gt=0)
    minimum_order_value: Decimal = Field(default=0, ge=0)
    expiry_date: datetime
    usage_limit: int = Field(gt=0)
    is_active: bool = True


class CouponResponse(BaseModel):
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    minimum_order_value: Decimal
    expiry_date: datetime
    usage_limit: int
    used_count: int
    is_active: bool

    class Config:
        from_attributes = True