from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.coupon import Coupon
from app.models.customer import Customer
from app.schemas.coupon import CouponCreate, CouponResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/coupons", tags=["Coupons"])


def get_admin_user(
    current_user: Customer = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


@router.post(
    "/",
    response_model=CouponResponse,
    status_code=201
)
def create_coupon(
    data: CouponCreate,
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_admin_user)
):
    existing = db.query(Coupon).filter(
        Coupon.code == data.code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Coupon code already exists"
        )

    if data.discount_type not in ["percentage", "flat"]:
        raise HTTPException(
            status_code=400,
            detail="Discount type must be percentage or flat"
        )

    if data.discount_type == "percentage" and data.discount_value > 100:
        raise HTTPException(
            status_code=400,
            detail="Percentage discount cannot exceed 100"
        )

    coupon = Coupon(
        code=data.code,
        discount_type=data.discount_type,
        discount_value=data.discount_value,
        minimum_order_value=data.minimum_order_value,
        expiry_date=data.expiry_date,
        usage_limit=data.usage_limit,
        is_active=data.is_active,
        used_count=0
    )

    db.add(coupon)
    db.commit()
    db.refresh(coupon)

    return coupon


@router.get(
    "/{code}",
    response_model=CouponResponse
)
def get_coupon(
    code: str,
    db: Session = Depends(get_db)
):
    coupon = db.query(Coupon).filter(
        Coupon.code == code
    ).first()

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found"
        )

    return coupon


@router.post("/{code}/apply")
def apply_coupon(
    code: str,
    order_amount: Decimal,
    db: Session = Depends(get_db)
):
    coupon = db.query(Coupon).filter(
        Coupon.code == code
    ).first()

    if not coupon:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found"
        )

    if not coupon.is_active:
        raise HTTPException(
            status_code=400,
            detail="Coupon is inactive"
        )

    if datetime.now() > coupon.expiry_date:
        raise HTTPException(
            status_code=400,
            detail="Coupon has expired"
        )

    if coupon.used_count >= coupon.usage_limit:
        raise HTTPException(
            status_code=400,
            detail="Coupon usage limit reached"
        )

    if order_amount < coupon.minimum_order_value:
        raise HTTPException(
            status_code=400,
            detail="Minimum order value not met"
        )

    if coupon.discount_type == "percentage":
        discount = (
            order_amount * coupon.discount_value / Decimal("100")
        )
    else:
        discount = coupon.discount_value

    if discount > order_amount:
        discount = order_amount

    final_amount = order_amount - discount

    coupon.used_count += 1
    db.commit()

    return {
        "coupon_code": coupon.code,
        "order_amount": float(order_amount),
        "discount": float(discount),
        "final_amount": float(final_amount)
    }