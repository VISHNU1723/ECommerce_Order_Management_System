from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.models.return_request import ReturnRequest
from app.schemas.return_schema import ReturnCreate, ReturnResponse

router = APIRouter(
    prefix="/returns",
    tags=["Returns"]
)


@router.post(
    "/{customer_id}/{order_id}",
    response_model=ReturnResponse,
    status_code=201
)
def create_return(
    customer_id: int,
    order_id: int,
    return_data: ReturnCreate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.customer_id == customer_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status not in ["Delivered"]:
        raise HTTPException(
            status_code=400,
            detail="Only delivered orders can be returned"
        )

    existing_return = db.query(ReturnRequest).filter(
        ReturnRequest.order_id == order_id
    ).first()

    if existing_return:
        raise HTTPException(
            status_code=400,
            detail="Return request already exists for this order"
        )

    return_request = ReturnRequest(
        order_id=order_id,
        customer_id=customer_id,
        reason=return_data.reason,
        status="Requested",
        refund_amount=Decimal(str(order.grand_total))
    )

    db.add(return_request)
    db.commit()
    db.refresh(return_request)

    return return_request


@router.get(
    "/{return_id}",
    response_model=ReturnResponse
)
def get_return(
    return_id: int,
    db: Session = Depends(get_db)
):
    return_request = db.query(ReturnRequest).filter(
        ReturnRequest.id == return_id
    ).first()

    if not return_request:
        raise HTTPException(
            status_code=404,
            detail="Return request not found"
        )

    return return_request

from typing import Optional


@router.put(
    "/{return_id}/status",
    response_model=ReturnResponse
)
def update_return_status(
    return_id: int,
    status: str,
    rejection_reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return_request = db.query(ReturnRequest).filter(
        ReturnRequest.id == return_id
    ).first()

    if not return_request:
        raise HTTPException(
            status_code=404,
            detail="Return request not found"
        )

    allowed_statuses = [
        "Requested",
        "Approved",
        "Rejected",
        "Refunded"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid return status"
        )

    if status == "Rejected" and not rejection_reason:
        raise HTTPException(
            status_code=400,
            detail="Rejection reason is required"
        )

    return_request.status = status

    if status == "Rejected":
        return_request.rejection_reason = rejection_reason

    db.commit()
    db.refresh(return_request)

    return return_request