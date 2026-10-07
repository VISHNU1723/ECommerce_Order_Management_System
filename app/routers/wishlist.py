from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate, WishlistResponse

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post(
    "/{customer_id}",
    response_model=WishlistResponse,
    status_code=201
)
def add_to_wishlist(
    customer_id: int,
    data: WishlistCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(404, "Customer not found")

    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    existing = db.query(Wishlist).filter(
        Wishlist.customer_id == customer_id,
        Wishlist.product_id == data.product_id
    ).first()

    if existing:
        raise HTTPException(400, "Product already in wishlist")

    wishlist = Wishlist(
        customer_id=customer_id,
        product_id=data.product_id
    )

    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return wishlist


@router.get(
    "/{customer_id}",
    response_model=list[WishlistResponse]
)
def get_wishlist(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(404, "Customer not found")

    return db.query(Wishlist).filter(
        Wishlist.customer_id == customer_id
    ).all()


@router.delete("/{customer_id}/{wishlist_id}")
def remove_from_wishlist(
    customer_id: int,
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    wishlist = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.customer_id == customer_id
    ).first()

    if not wishlist:
        raise HTTPException(404, "Wishlist item not found")

    db.delete(wishlist)
    db.commit()

    return {"message": "Product removed from wishlist"}


@router.post("/{customer_id}/{wishlist_id}/move-to-cart")
def move_to_cart(
    customer_id: int,
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    wishlist = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.customer_id == customer_id
    ).first()

    if not wishlist:
        raise HTTPException(404, "Wishlist item not found")

    cart = db.query(Cart).filter(
        Cart.customer_id == customer_id
    ).first()

    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.flush()

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == wishlist.product_id
    ).first()

    if not existing_item:
        db.add(
            CartItem(
                cart_id=cart.id,
                product_id=wishlist.product_id,
                quantity=1
            )
        )

    db.delete(wishlist)
    db.commit()

    return {"message": "Product moved to cart successfully"}