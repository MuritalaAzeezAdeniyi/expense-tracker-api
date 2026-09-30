import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main as main_module
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    app.state.users.clear()
    app.state.expenses.clear()
    yield
    app.state.users.clear()
    app.state.expenses.clear()


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
    original_payload = {
        "full_name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "StrongPass1!",
    }

    first_response = client.post("/register", json=original_payload)
    assert first_response.status_code == 201

    duplicate_payload = {
        "full_name": "Another User",
        "email": "DUPLICATE@example.com",
        "password": "AnotherStrongPass1!",
    }

    second_response = client.post("/register", json=duplicate_payload)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "A user with this email address already exists."

    stored_users = list(app.state.users.values())
    assert len(stored_users) == 1
    assert stored_users[0]["full_name"] == original_payload["full_name"]
    assert stored_users[0]["email"] == original_payload["email"].lower()
    assert stored_users[0]["password_hash"]


def test_production_code_does_not_hardcode_secrets():
    app_root = Path(main_module.__file__).resolve().parent
    source_files = app_root.rglob("*.py")
    violations = []

    for file_path in source_files:
        text = file_path.read_text(encoding="utf-8")
        if re.search(
            r"(?i)(?:jwt[_-]?secret|secret[_-]?key|api[_-]?key|database[_-]?password|db[_-]?password)\s*[:=]\s*['\"]",
            text,
        ):
            violations.append(str(file_path.relative_to(app_root)))

    assert not violations, f"Hardcoded secrets detected in app code: {violations}"

    auth_service_source = (app_root / "services" / "auth_service.py").read_text(encoding="utf-8")
    assert 'os.getenv("JWT_SECRET_KEY")' in auth_service_source


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


def test_password_is_never_exposed_in_registration_response_or_storage():
    payload = {
        "full_name": "Password Protection",
        "email": "passwordprotection@example.com",
        "password": "StrongPass1!",
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 201

    body = response.json()
    assert body["full_name"] == payload["full_name"]
    assert body["email"] == payload["email"]
    assert "password" not in body
    assert "password_hash" not in body

    stored_user = next(
        user for user in app.state.users.values() if user["email"] == payload["email"]
    )
    assert stored_user["password_hash"] != payload["password"]
    assert "password" not in stored_user
    assert stored_user["password_hash"]

    login_response = client.post(
        "/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )
    assert login_response.status_code == 200
    assert login_response.json()["email"] == payload["email"]
    assert "password" not in login_response.json()
    assert "password_hash" not in login_response.json()
