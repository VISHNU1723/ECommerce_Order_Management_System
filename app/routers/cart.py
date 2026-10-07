from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.customer import Customer
from app.models.product import Product
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get("/{customer_id}", response_model=CartResponse)
def get_cart(
    customer_id: int,
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(
        Cart.customer_id == customer_id
    ).first()

    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


@router.post(
    "/{customer_id}/items",
    response_model=CartResponse
)
def add_to_cart(
    customer_id: int,
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    cart = db.query(Cart).filter(
        Cart.customer_id == customer_id
    ).first()

    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart)

    return cart


@router.put(
    "/{customer_id}/items/{item_id}",
    response_model=CartResponse
)
def update_cart_item(
    customer_id: int,
    item_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(
        Cart.customer_id == customer_id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.quantity = item.quantity

    db.commit()
    db.refresh(cart)

    return cart


@router.delete(
    "/{customer_id}/items/{item_id}"
)
def remove_from_cart(
    customer_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(
        Cart.customer_id == customer_id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Cart item removed successfully"
    }