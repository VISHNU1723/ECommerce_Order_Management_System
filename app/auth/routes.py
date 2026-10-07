from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_customer = (
        db.query(Customer)
        .filter(Customer.email == data.email)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    customer = Customer(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role="customer"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer registered successfully",
        "customer_id": customer.id
    }


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.email == data.email)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, customer.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(customer.id),
            "email": customer.email,
            "role": customer.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: Customer = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
    }