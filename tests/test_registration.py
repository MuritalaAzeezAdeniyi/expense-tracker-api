from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_success():
    payload = {
        "full_name": "Alice Example",
        "email": "alice@example.com",
        "password": "StrongPass1!",
    }

    response = client.post("/register", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["full_name"] == payload["full_name"]
    assert body["email"] == payload["email"]
    assert body["id"]
    assert "password" not in body
    assert "password_hash" not in body


def test_register_missing_required_fields():
    response = client.post(
        "/register",
        json={"full_name": "Missing Email", "password": "StrongPass1!"},
    )

    assert response.status_code == 422


def test_register_invalid_email():
    response = client.post(
        "/register",
        json={
            "full_name": "Bad Email",
            "email": "not-an-email",
            "password": "StrongPass1!",
        },
    )

    assert response.status_code == 422


def test_register_duplicate_email():
    payload = {
        "full_name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "StrongPass1!",
    }

    first_response = client.post("/register", json=payload)
    assert first_response.status_code == 201

    second_response = client.post("/register", json=payload)

    assert second_response.status_code == 409


def test_password_is_hashed_before_storage():
    payload = {
        "full_name": "Hash Check",
        "email": "hashcheck@example.com",
        "password": "StrongPass1!",
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 201

    stored_user = next(
        user for user in app.state.users.values() if user["email"] == payload["email"]
    )

    assert stored_user["password_hash"] != payload["password"]
    assert "password" not in stored_user
    assert stored_user["password_hash"]
