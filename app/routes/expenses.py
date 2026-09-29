from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.expense import ALLOWED_CATEGORIES, ExpenseCreate, ExpenseResponse, ExpenseUpdate
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


@router.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    request: Request,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    if category is not None and category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Category must be one of: Food, Transportation, Housing, Utilities, Health, Education, Entertainment, Shopping, Other.")

    user = get_authenticated_user(request.app.state.users, credentials.credentials)
    expenses = [
        expense
        for expense in request.app.state.expenses.values()
        if expense["user_id"] == user["id"]
    ]

    if category is not None:
        expenses = [expense for expense in expenses if expense["category"] == category]
    if start_date is not None:
        expenses = [expense for expense in expenses if expense["expense_date"] >= start_date]
    if end_date is not None:
        expenses = [expense for expense in expenses if expense["expense_date"] <= end_date]

    return expenses


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    request: Request,
    expense_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    user = get_authenticated_user(request.app.state.users, credentials.credentials)
    expense = request.app.state.expenses.get(expense_id)
    if expense is None or expense["user_id"] != user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")

    return expense


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    request: Request,
    expense_id: str,
    updates: ExpenseUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    user = get_authenticated_user(request.app.state.users, credentials.credentials)
    expense = request.app.state.expenses.get(expense_id)
    if expense is None or expense["user_id"] != user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")

    expense["amount"] = Decimal(str(updates.amount))
    expense["description"] = updates.description
    expense["category"] = updates.category
    expense["expense_date"] = updates.expense_date
    expense["updated_at"] = datetime.now(timezone.utc)

    return expense


@router.delete("/expenses/{expense_id}")
def delete_expense(
    request: Request,
    expense_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    user = get_authenticated_user(request.app.state.users, credentials.credentials)
    expense = request.app.state.expenses.get(expense_id)
    if expense is None or expense["user_id"] != user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")

    del request.app.state.expenses[expense_id]
    return {"detail": "Expense deleted successfully."}
