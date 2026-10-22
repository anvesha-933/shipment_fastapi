from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session

from auth import oauth_scheme, verify_token
from database.models import User
from database.sessions import get_session
from repositories.tokens import is_token_revoked


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth_scheme),
    session: Session = Depends(get_session),
) -> User:
    token = credentials.credentials
    if is_token_revoked(token, session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked, please log in again",
        )

    user_id = verify_token(token)
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
