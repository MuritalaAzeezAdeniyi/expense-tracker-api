from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    expense_date: date

    @field_validator("description", "category")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("This field is required.")
        return cleaned


class ExpenseUpdate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    expense_date: date

    @field_validator("description", "category")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("This field is required.")
        return cleaned


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    amount: Decimal
    description: str
    category: str
    expense_date: date
    created_at: datetime
    updated_at: datetime
