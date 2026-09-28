from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.auth_service import get_authenticated_user

router = APIRouter(prefix="", tags=["expenses"])
security = HTTPBearer(auto_error=False)


@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    request: Request,
    expense: ExpenseCreate,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    user = get_authenticated_user(request.app.state.users, credentials.credentials)
    expense_id = str(uuid4())
    now = datetime.now(timezone.utc)
    expense_record = {
        "id": expense_id,
        "user_id": user["id"],
        "amount": Decimal(str(expense.amount)),
        "description": expense.description,
        "category": expense.category,
        "expense_date": expense.expense_date,
        "created_at": now,
        "updated_at": now,
    }
    request.app.state.expenses[expense_id] = expense_record

    return {
        "id": expense_record["id"],
        "user_id": expense_record["user_id"],
        "amount": expense_record["amount"],
        "description": expense_record["description"],
        "category": expense_record["category"],
        "expense_date": expense_record["expense_date"],
        "created_at": expense_record["created_at"],
        "updated_at": expense_record["updated_at"],
    }
