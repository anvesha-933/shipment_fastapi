from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session

from auth import oauth_scheme, verify_token
from controllers.dependencies import get_current_user
from database.models import User
from database.sessions import get_session
from schemas import LoginResponse, LoginUser, UserCreate, UserResponse
from services.exceptions import InvalidCredentials, UserAlreadyExists
from services.users import authenticate_user, create_user, logout_user


router = APIRouter()


@router.post(
    "/create-user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(data: UserCreate, session: Session = Depends(get_session)):
    try:
        return create_user(data, session)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already taken",
        )


@router.post("/login", response_model=LoginResponse)
def login(data: LoginUser, session: Session = Depends(get_session)):
    try:
        user, user_id, token = authenticate_user(data, session)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return LoginResponse(
        message="Login successful",
        userid=user_id,
        username=user.username,
        email=user.email,
        token=token,
    )


@router.get("/users/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(oauth_scheme),
    session: Session = Depends(get_session),
):
    token = credentials.credentials
    verify_token(token)
    logout_user(token, session)
    return {"message": "Logged out successfully"}
