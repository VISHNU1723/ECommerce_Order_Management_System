from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ReturnCreate(BaseModel):
    reason: str


class ReturnResponse(BaseModel):
    id: int
    order_id: int
    customer_id: int
    reason: str
    status: str
    refund_amount: Optional[Decimal] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True