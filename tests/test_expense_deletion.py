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


def test_delete_own_expense_successfully():
    token = _register_and_login("owner@example.com", "Owner")
    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "25.00",
            "description": "Groceries",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.delete(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Expense deleted successfully."
    assert expense_id not in app.state.expenses


def test_deleted_expense_cannot_be_retrieved():
    token = _register_and_login("owner@example.com", "Owner")
    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.00",
            "description": "Coffee",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200

    retrieve_response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert retrieve_response.status_code == 404
    assert retrieve_response.json()["detail"] == "Expense not found."


def test_delete_nonexistent_expense_returns_404():
    token = _register_and_login("missing@example.com", "Missing")

    response = client.delete(
        "/expenses/does-not-exist",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."


def test_user_cannot_delete_another_users_expense():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "60.00",
            "description": "Hotel",
            "category": "Housing",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.delete(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."
    assert expense_id in app.state.expenses


def test_unauthenticated_delete_is_rejected():
    response = client.delete("/expenses/any-id")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated."
