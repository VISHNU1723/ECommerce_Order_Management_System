from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.address import Address
from app.models.customer import Customer
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse


router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/{customer_id}", response_model=AddressResponse, status_code=201)
def create_address(
    customer_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if address.is_default:
        db.query(Address).filter(
            Address.customer_id == customer_id
        ).update({"is_default": False})

    new_address = Address(
        customer_id=customer_id,
        full_name=address.full_name,
        phone=address.phone,
        address_line=address.address_line,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        is_default=address.is_default
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address


@router.get("/{customer_id}", response_model=list[AddressResponse])
def get_addresses(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return db.query(Address).filter(
        Address.customer_id == customer_id
    ).all()


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db)
):
    address = db.query(Address).filter(
        Address.id == address_id
    ).first()

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    update_data = address_data.model_dump(exclude_unset=True)

    if update_data.get("is_default") is True:
        db.query(Address).filter(
            Address.customer_id == address.customer_id
        ).update({"is_default": False})

    for key, value in update_data.items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    return address


@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db)
):
    address = db.query(Address).filter(
        Address.id == address_id
    ).first()

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    db.delete(address)
    db.commit()

    return {"message": "Address deleted successfully"}


@router.put("/{address_id}/default", response_model=AddressResponse)
def set_default_address(
    address_id: int,
    db: Session = Depends(get_db)
):
    address = db.query(Address).filter(
        Address.id == address_id
    ).first()

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    db.query(Address).filter(
        Address.customer_id == address.customer_id
    ).update({"is_default": False})

    address.is_default = True

    db.commit()
    db.refresh(address)

    return address