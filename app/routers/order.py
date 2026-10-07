from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.customer import Customer
from app.models.address import Address
from app.models.cart import Cart
from app.schemas.order import OrderResponse
from app.models.product import Product
from app.services.email_service import send_email


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/{customer_id}",
    response_model=OrderResponse,
    status_code=201
)

def create_order(
    customer_id: int,
    address_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        address = db.query(Address).filter(
            Address.id == address_id,
            Address.customer_id == customer_id
        ).first()

        if not address:
            raise HTTPException(
                status_code=404,
                detail="Address not found"
            )

        cart = db.query(Cart).filter(
            Cart.customer_id == customer_id
        ).first()

        if not cart or not cart.items:
            raise HTTPException(
                status_code=400,
                detail="Cart is empty"
            )

        subtotal = Decimal("0.00")

        for cart_item in cart.items:
            product = cart_item.product

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )

            if not product.is_active:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product '{product.name}' is inactive"
                )

            if cart_item.quantity > product.stock_quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {product.name}"
                )

            subtotal += (
                Decimal(str(product.price))
                * cart_item.quantity
            )

        tax_amount = (
            subtotal * Decimal("0.18")
        ).quantize(Decimal("0.01"))

        if subtotal > Decimal("500.00"):
            delivery_charge = Decimal("0.00")
        else:
            delivery_charge = Decimal("50.00")

        grand_total = (
            subtotal
            + tax_amount
            + delivery_charge
        ).quantize(Decimal("0.01"))

        today = datetime.now().strftime("%Y%m%d")
        prefix = f"ORD-{today}-"

        today_count = db.query(Order).filter(
            Order.order_number.like(f"{prefix}%")
        ).count()

        order_number = f"{prefix}{today_count + 1:04d}"

        order = Order(
            order_number=order_number,
            customer_id=customer_id,
            address_id=address_id,
            subtotal=subtotal,
            tax_amount=tax_amount,
            delivery_charge=delivery_charge,
            grand_total=grand_total,
            status="Pending",
            payment_status="Unpaid"
        )

        db.add(order)
        db.flush()

        for cart_item in cart.items:
            product = cart_item.product

            line_total = (
                Decimal(str(product.price))
                * cart_item.quantity
            ).quantize(Decimal("0.01"))

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=cart_item.quantity,
                unit_price=product.price,
                line_total=line_total
            )

            product.stock_quantity -= cart_item.quantity

            db.add(order_item)

        for cart_item in list(cart.items):
            db.delete(cart_item)

        db.commit()
        db.refresh(order)

        background_tasks.add_task(
            send_email,
            customer.email,
            "Order Confirmation",
            f"Your order {order.order_number} has been placed successfully. "
            f"Total amount: ₹{order.grand_total}"
)


        return order

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create order"
        )

@router.put(
    "/{order_id}/cancel",
    response_model=OrderResponse
)
def cancel_order(
    order_id: int,
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

    if order.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    for item in order.items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product:
            product.stock_quantity += item.quantity

    order.status = "Cancelled"

    db.commit()
    db.refresh(order)

    return order

@router.put(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status: str,
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

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order.status = status

    if status == "Delivered":
        order.delivered_at = datetime.now()

    db.commit()
    db.refresh(order)

    if status == "Shipped":
        background_tasks.add_task(
            send_email,
            order.customer.email,
            "Order Shipped",
            f"Your order {order.order_number} has been shipped successfully."
    )


    return order

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
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

    return order


@router.get(
    "/customer/{customer_id}",
    response_model=list[OrderResponse]
)
def get_customer_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).all()

    return orders