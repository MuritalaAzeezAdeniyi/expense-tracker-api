import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_users():
    app.state.users.clear()
    yield
    app.state.users.clear()


def test_login_success():
    client.post(
        "/register",
        json={
            "full_name": "Alice Example",
            "email": "alice@example.com",
            "password": "StrongPass1!",
        },
    )

    response = client.post(
        "/login",
        json={
            "email": "alice@example.com",
            "password": "StrongPass1!",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert body["full_name"] == "Alice Example"
    assert "password" not in body
    assert "password_hash" not in body


def test_login_invalid_credentials():
    client.post(
        "/register",
        json={
            "full_name": "Alice Example",
            "email": "alice@example.com",
            "password": "StrongPass1!",
        },
    )

    response = client.post(
        "/login",
        json={
            "email": "alice@example.com",
            "password": "WrongPassword1!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."
