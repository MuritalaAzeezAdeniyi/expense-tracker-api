import base64
import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt
from fastapi import HTTPException, status

from app.schemas.auth import LoginRequest, UserCreate


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii")
    hash_b64 = base64.urlsafe_b64encode(derived).decode("ascii")
    return f"pbkdf2_sha256$100000${salt_b64}${hash_b64}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations_raw, salt_b64, hash_b64 = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations_raw)
        salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        computed_hash = base64.urlsafe_b64encode(derived).decode("ascii")
        return computed_hash == hash_b64
    except (ValueError, TypeError):
        return False


def register_user(users_store: dict[str, dict[str, Any]], user_data: UserCreate) -> dict[str, Any]:
    normalized_email = user_data.email.lower().strip()

    for existing in users_store.values():
        if existing["email"].lower() == normalized_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email address already exists.",
            )

    now = datetime.now(timezone.utc) 
    user_id = str(uuid4())
    user_record = {
        "id": user_id,
        "full_name": user_data.full_name,
        "email": normalized_email,
        "password_hash": _hash_password(user_data.password),
        "created_at": now,
        "updated_at": now,
    }

    users_store[user_id] = user_record

    return {
        "id": user_record["id"],
        "full_name": user_record["full_name"],
        "email": user_record["email"],
        "created_at": user_record["created_at"],
        "updated_at": user_record["updated_at"],
    }


def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT secret is not configured.",
        )
    return secret


def login_user(users_store: dict[str, dict[str, Any]], credentials: LoginRequest) -> dict[str, Any]:
    normalized_email = credentials.email.lower().strip()
    user_record = next(
        (user for user in users_store.values() if user["email"].lower() == normalized_email),
        None,
    )

    if user_record is None or not _verify_password(credentials.password, user_record["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = jwt.encode(
        {
            "sub": user_record["id"],
            "email": user_record["email"],
            "full_name": user_record["full_name"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        _get_jwt_secret(),
        algorithm="HS256",
    )
    return {
        "id": user_record["id"],
        "full_name": user_record["full_name"],
        "email": user_record["email"],
        "token": token,
    }


def get_authenticated_user(users_store: dict[str, dict[str, Any]], token: str) -> dict[str, Any]:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    try:
        payload = jwt.decode(
            token,
            _get_jwt_secret(),
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.") from None
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.") from None

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")

    user_record = next((user for user in users_store.values() if user["id"] == user_id), None)
    if user_record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")

    return {
        "id": user_record["id"],
        "full_name": user_record["full_name"],
        "email": user_record["email"],
    }
