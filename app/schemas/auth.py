from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Full name is required.")
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(ch.isupper() for ch in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(ch.islower() for ch in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(ch.isdigit() for ch in value):
            raise ValueError("Password must contain at least one number.")
        if not any(not ch.isalnum() for ch in value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
