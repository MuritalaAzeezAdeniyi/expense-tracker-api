import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient

from app.main import app


os.environ["JWT_SECRET_KEY"] = "32-character-secret-key-for-testing-123"

client = TestClient(app)


def test_protected_route_requires_authentication():
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated."


def test_protected_route_rejects_invalid_token():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication token."


def test_protected_route_rejects_expired_token():
    expired_token = jwt.encode(
        {
            "sub": "user-123",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        os.environ["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired."


def test_valid_token_allows_access():
    register_response = client.post(
        "/register",
        json={
            "full_name": "JWT User",
            "email": "jwtuser@example.com",
            "password": "StrongPass1!",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json={
            "email": "jwtuser@example.com",
            "password": "StrongPass1!",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["token"]

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "jwtuser@example.com"
    assert response.json()["full_name"] == "JWT User"
