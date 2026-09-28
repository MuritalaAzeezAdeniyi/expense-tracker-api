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


def test_get_expenses_returns_only_current_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    expense_a = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "12.50",
            "description": "Coffee",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    assert expense_a.status_code == 201

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "99.00",
            "description": "Train ticket",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["description"] == "Coffee"
    assert body[0]["user_id"]


def test_get_expense_by_id_returns_owned_expense():
    token = _register_and_login("owner@example.com", "Owner")
    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "25.00",
            "description": "Lunch",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == expense_id
    assert response.json()["description"] == "Lunch"


def test_get_expense_by_id_returns_404_when_expense_does_not_exist():
    token = _register_and_login("missing@example.com", "Missing")

    response = client.get(
        "/expenses/does-not-exist",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."


def test_get_expense_by_id_returns_404_for_another_users_expense():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "41.50",
            "description": "Hotel",
            "category": "Housing",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."


def test_get_expenses_rejects_cross_user_access():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "10.00",
            "description": "Taxi",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert response.json() == []
