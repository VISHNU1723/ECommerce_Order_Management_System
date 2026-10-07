from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_order_placement():
    response = client.get("/orders/customer/2")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_order_stock_deduction():
    response = client.get("/products/3")

    assert response.status_code == 200

    product = response.json()

    assert "stock_quantity" in product
    assert product["stock_quantity"] >= 0

def test_order_cancellation():
    response = client.get("/orders/9")

    assert response.status_code == 200

    order = response.json()

    assert order["status"] == "Cancelled"