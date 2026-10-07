from pydantic import BaseModel, Field, ConfigDict


class AddressCreate(BaseModel):
    full_name: str
    phone: str = Field(min_length=10, max_length=10)
    address_line: str
    city: str
    state: str
    pincode: str = Field(min_length=6, max_length=6)
    is_default: bool = False


class AddressUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = Field(default=None, min_length=10, max_length=10)
    address_line: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = Field(default=None, min_length=6, max_length=6)
    is_default: bool | None = None


class AddressResponse(BaseModel):
    id: int
    customer_id: int
    full_name: str
    phone: str
    address_line: str
    city: str
    state: str
    pincode: str
    is_default: bool

    model_config = ConfigDict(from_attributes=True)