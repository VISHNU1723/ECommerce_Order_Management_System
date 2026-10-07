from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine
from app.auth.routes import router as auth_router
from app.routers.product import router as product_router
from app.routers.category import router as category_router
from app.routers.cart import router as cart_router
from app.routers.address import router as address_router
from app.routers.order import router as order_router
from app.routers.payment import router as payment_router
from app.routers.return_router import router as return_router
from app.routers.review import router as review_router
from app.routers import report
from app.routers import wishlist
from app.routers import coupon

app = FastAPI(
    title="E-Commerce Order Management System",
    version="1.0.0",
    description="Backend API for E-Commerce Order Management"
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(address_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(return_router)
app.include_router(review_router)
app.include_router(report.router)
app.include_router(wishlist.router)
app.include_router(coupon.router)

@app.get("/")
def root():
    return {
        "message": "E-Commerce Order Management System API is running"
    }


@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database": "connected",
            "result": result.scalar()
        }