from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.return_request import ReturnRequest
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


# Admin-only check
def get_admin_user(
    current_user: Customer = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


# 1. Sales Report
@router.get("/sales")
def sales_report(
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_admin_user)
):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        total_orders = (
            db.query(Order)
            .filter(
                Order.created_at >= start,
                Order.created_at < end.replace(
                    hour=23, minute=59, second=59
                )
            )
            .count()
        )

        total_revenue = (
            db.query(func.coalesce(func.sum(Order.grand_total), 0))
            .filter(
                Order.created_at >= start,
                Order.created_at < end.replace(
                    hour=23, minute=59, second=59
                ),
                Order.payment_status == "Paid"
            )
            .scalar()
        )

        total_refunds = (
            db.query(func.coalesce(func.sum(ReturnRequest.refund_amount), 0))
            .filter(
                ReturnRequest.created_at >= start,
                ReturnRequest.created_at < end.replace(
                    hour=23, minute=59, second=59
                ),
                ReturnRequest.status == "Refunded"
            )
            .scalar()
        )

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_orders": total_orders,
            "total_revenue": float(total_revenue),
            "total_refunds": float(total_refunds)
        }

    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Date must be in YYYY-MM-DD format"
        )


# 2. Orders by Status
@router.get("/orders-by-status")
def orders_by_status(
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_admin_user)
):
    results = (
        db.query(
            Order.status,
            func.count(Order.id).label("order_count")
        )
        .group_by(Order.status)
        .all()
    )

    return {
        "orders_by_status": [
            {
                "status": status,
                "order_count": count
            }
            for status, count in results
        ]
    }


# 3. Top 5 Products
@router.get("/top-products")
def top_products(
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_admin_user)
):
    results = (
        db.query(
            Product.id,
            Product.name,
            func.sum(OrderItem.quantity).label("quantity_sold")
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status != "Cancelled")
        .group_by(Product.id, Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    return {
        "top_products": [
            {
                "product_id": product_id,
                "product_name": product_name,
                "quantity_sold": quantity_sold
            }
            for product_id, product_name, quantity_sold in results
        ]
    }


# 4. Low Stock Products
@router.get("/low-stock")
def low_stock_products(
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_admin_user)
):
    products = (
        db.query(Product)
        .filter(Product.stock_quantity < 5)
        .order_by(Product.stock_quantity.asc())
        .all()
    )

    return [
        {
            "product_id": product.id,
            "product_name": product.name,
            "stock_quantity": product.stock_quantity
        }
        for product in products
    ]