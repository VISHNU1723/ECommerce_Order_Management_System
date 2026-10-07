import uuid
from decimal import Decimal

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.email_service import send_email

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/{order_id}",
    response_model=PaymentResponse,
    status_code=201
)
def create_payment(
    order_id: int,
    payment_data: PaymentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Cannot make payment for a cancelled order"
        )

    if order.payment_status == "Paid":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid"
        )

    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

    payment = Payment(
        order_id=order.id,
        amount=Decimal(str(order.grand_total)),
        payment_method=payment_data.payment_method,
        transaction_id=transaction_id,
        status="Success"
    )

    order.payment_status = "Paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    background_tasks.add_task(
        send_email,
        order.customer.email,
        "Payment Successful",
        f"Your payment for Order #{order.order_number} was successful. "
        f"Amount paid: ₹{order.grand_total}. "
        f"Transaction ID: {transaction_id}"
)

    return payment


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment