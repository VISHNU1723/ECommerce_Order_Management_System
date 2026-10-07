from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    payment_method: str
    transaction_id: str
    status: str

    model_config = ConfigDict(from_attributes=True)