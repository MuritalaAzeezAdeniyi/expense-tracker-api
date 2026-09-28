from fastapi import APIRouter, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import LoginRequest, LoginResponse, UserCreate, UserResponse
from app.services.auth_service import get_authenticated_user, login_user, register_user

router = APIRouter(prefix="", tags=["auth"])
security = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: Request, user: UserCreate):
    return register_user(request.app.state.users, user)


@router.post("/login", response_model=LoginResponse)
def login(request: Request, credentials: LoginRequest):
    return login_user(request.app.state.users, credentials)


@router.get("/protected")
def protected_route(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    user = get_authenticated_user(request.app.state.users, credentials.credentials)
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
    }
