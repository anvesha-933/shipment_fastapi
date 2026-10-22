from sqlmodel import Session

from auth import create_access_token
from database.models import User
from hash import check_password, generate_password
from repositories import tokens as token_repository
from repositories import users as user_repository
from schemas import LoginUser, UserCreate
from services.exceptions import InvalidCredentials, UserAlreadyExists


def create_user(data: UserCreate, session: Session) -> User:
    existing_user = user_repository.get_by_username_or_email(
        data.username, str(data.email), session
    )
    if existing_user:
        raise UserAlreadyExists()

    user = User(
        username=data.username,
        email=str(data.email),
        password_hash=generate_password(data.password),
    )
    return user_repository.add(user, session)


def authenticate_user(data: LoginUser, session: Session) -> tuple[User, int, str]:
    user = user_repository.get_by_email(str(data.email), session)
    if user is None or not check_password(data.password, user.password_hash):
        raise InvalidCredentials()
    if user.id is None:
        raise RuntimeError("Authenticated user is missing its database ID")

    return user, user.id, create_access_token(user.id)


def logout_user(token: str, session: Session) -> None:
    token_repository.revoke(token, session)
