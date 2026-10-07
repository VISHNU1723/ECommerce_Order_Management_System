# E-Commerce Order Management System

A FastAPI-based backend application for managing customers, products, carts, orders, payments, returns, reviews, reports, coupons, and wishlists.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- MySQL
- Alembic
- JWT Authentication
- Passlib / bcrypt
- Pytest
- Uvicorn
- SMTP Email / BackgroundTasks

## Main Features

### Authentication
- Customer registration
- Customer login
- JWT authentication
- Get current user
- Password hashing using bcrypt

### Product & Category Management
- Create categories
- Manage products
- Product search
- Category filtering
- Price filtering
- Sorting
- Pagination

### Cart Management
- Add product to cart
- View cart
- Update cart quantity
- Remove cart item

### Address Management
- Create address
- Get address
- Update address
- Set default address
- Delete address

### Order Management
- Create order
- Calculate subtotal
- Calculate GST
- Calculate delivery charge
- Deduct product stock
- Cancel order
- Update order status
- View order
- View customer orders

### Payments
- Create payment
- Generate transaction ID
- Update payment status
- Get payment details

### Returns
- Create return request
- Get return request
- Approve return
- Reject return

### Reviews
- Create product review
- Get review
- Rating validation
- Duplicate review prevention

### Reports
- Sales report
- Orders by status
- Top products
- Low-stock products

### Coupons
- Create coupon
- Get coupon
- Apply coupon

### Wishlist
- Add product to wishlist
- View wishlist
- Remove product from wishlist

### Email Notifications
- Order confirmation email
- Payment success email
- Background email processing using FastAPI BackgroundTasks

## Database

MySQL is used as the database.

Database name:

`ecommerce_order_db`

Database migrations are managed using Alembic.

## Project Structure

```text
ECommerce_Order_Management_System/
│
├── app/
│   ├── auth/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   └── test_orders.py
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md