from fastapi import APIRouter, Request, status

from app.schemas.auth import UserCreate, UserResponse
from app.services.auth_service import register_user

router = APIRouter(prefix="", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: Request, user: UserCreate):
    return register_user(request.app.state.users, user)
