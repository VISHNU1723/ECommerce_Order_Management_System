from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    category_id: int
    price: float
    stock_quantity: int = 0
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: Optional[str] = None
    category_id: int
    price: float
    stock_quantity: int
    is_active: bool

    class Config:
        from_attributes = True