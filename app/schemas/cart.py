from pydantic import BaseModel, Field
from typing import List


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    customer_id: int
    items: List[CartItemResponse] = []

    class Config:
        from_attributes = True