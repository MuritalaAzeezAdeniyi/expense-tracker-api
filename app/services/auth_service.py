import base64
import hashlib
import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import HTTPException, status

from app.schemas.auth import UserCreate


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii")
    hash_b64 = base64.urlsafe_b64encode(derived).decode("ascii")
    return f"pbkdf2_sha256$100000${salt_b64}${hash_b64}"


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
