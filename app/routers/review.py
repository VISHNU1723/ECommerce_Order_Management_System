from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.review import Review
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post(
    "/{customer_id}",
    response_model=ReviewResponse,
    status_code=201
)
def create_review(
    customer_id: int,
    review_data: ReviewCreate,
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
        Product.id == review_data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_review = db.query(Review).filter(
        Review.customer_id == customer_id,
        Review.product_id == review_data.product_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this product"
        )

    new_review = Review(
        customer_id=customer_id,
        product_id=review_data.product_id,
        rating=review_data.rating,
        comment=review_data.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.get(
    "/{review_id}",
    response_model=ReviewResponse
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(
        Review.id == review_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review