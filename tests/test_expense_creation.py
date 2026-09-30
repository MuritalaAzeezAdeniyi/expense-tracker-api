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


def test_create_expense_accepts_valid_category():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.50",
            "description": "Train ticket",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 201
    assert response.json()["category"] == "Transportation"


def test_create_expense_rejects_invalid_category():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Groceries",
            "category": "Travel",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 422


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
    assert len(app.state.expenses) == 0


def test_create_expense_rejects_negative_amount():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": -1,
            "description": "Groceries",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )

    assert response.status_code == 422
    assert len(app.state.expenses) == 0


def test_create_expense_rejects_invalid_body_format():
    token = _register_and_login()

    response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json=["not", "an", "expense"],
    )

    assert response.status_code == 422
    assert len(app.state.expenses) == 0


def test_create_expense_unexpected_error_returns_generic_500(monkeypatch):
    token = _register_and_login()

    def raise_unexpected_error(*args, **kwargs):
        raise RuntimeError("unexpected failure")

    monkeypatch.setattr("app.routes.expenses.get_authenticated_user", raise_unexpected_error)

    with TestClient(app, raise_server_exceptions=False) as test_client:
        response = test_client.post(
            "/expenses",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "amount": "10.00",
                "description": "Groceries",
                "category": "Food",
                "expense_date": "2026-09-28",
            },
        )

    assert response.status_code == 500
    payload = response.text
    assert payload == "Internal Server Error"
    serialized = payload.lower()
    assert "traceback" not in serialized
    assert "password" not in serialized
    assert "jwt" not in serialized
    assert "secret" not in serialized
    assert "file" not in serialized
    assert len(app.state.expenses) == 0


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
