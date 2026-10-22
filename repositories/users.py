from sqlmodel import Session, or_, select

from database.models import User


def get_by_email(email: str, session: Session) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def get_by_username_or_email(
    username: str, email: str, session: Session
) -> User | None:
    return session.exec(
        select(User).where(or_(User.username == username, User.email == email))
    ).first()


def add(user: User, session: Session) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
