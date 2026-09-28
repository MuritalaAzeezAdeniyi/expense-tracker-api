from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    app.state.users.clear()
    app.state.expenses.clear()
    yield
    app.state.users.clear()
    app.state.expenses.clear()


def _register_and_login(email: str = "expense@example.com") -> str:
    client.post(
        "/register",
        json={
            "full_name": "Expense User",
            "email": email,
            "password": "StrongPass1!",
        },
    )
    login_response = client.post(
        "/login",
        json={
            "email": email,
            "password": "StrongPass1!",
        },
    )
    return login_response.json()["token"]


def test_create_expense_successfully():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "49.99",
            "description": "Groceries",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["amount"] == "49.99"
    assert body["description"] == "Groceries"
    assert body["category"] == "Food"
    assert body["expense_date"] == "2026-09-28"
    assert body["user_id"]
    assert body["id"]


def test_create_expense_rejects_non_positive_amount():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": 0,
            "description": "Groceries",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 422


def test_create_expense_requires_description():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "   ",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 422


def test_create_expense_requires_category():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Groceries",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 422


def test_create_expense_requires_valid_date():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Groceries",
            "category": "Food",
            "expense_date": "not-a-date",
        },
    )

    assert response.status_code == 422
