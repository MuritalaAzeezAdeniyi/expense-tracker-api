import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


os.environ["JWT_SECRET_KEY"] = "32-character-secret-key-for-testing-123"

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    app.state.users.clear()
    app.state.expenses.clear()
    yield
    app.state.users.clear()
    app.state.expenses.clear()


def _register_and_login(email: str, full_name: str = "Expense User") -> str:
    client.post(
        "/register",
        json={
            "full_name": full_name,
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


def test_update_own_expense_successfully():
    token = _register_and_login("owner@example.com", "Owner")
    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "20.00",
            "description": "Original",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "35.50",
            "description": "Updated lunch",
            "category": "Food",
            "expense_date": "2026-09-29",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == expense_id
    assert body["amount"] == "35.50"
    assert body["description"] == "Updated lunch"
    assert body["category"] == "Food"
    assert body["expense_date"] == "2026-09-29"
    assert body["user_id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_update_expense_rejects_invalid_values():
    token = _register_and_login("invalid@example.com", "Invalid")
    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Valid",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": 0,
            "description": "   ",
            "category": "",
            "expense_date": "not-a-date",
        },
    )

    assert response.status_code == 422


def test_update_expense_rejects_cross_user_access():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "50.00",
            "description": "Hotel",
            "category": "Housing",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "75.00",
            "description": "Stolen update",
            "category": "Food",
            "expense_date": "2026-09-29",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."
