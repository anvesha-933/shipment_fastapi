from sqlmodel import Session, select

from database.models import RevokedToken


def is_token_revoked(token: str, session: Session) -> bool:
    revoked = session.exec(
        select(RevokedToken).where(RevokedToken.token == token)
    ).first()
    return revoked is not None


def revoke(token: str, session: Session) -> None:
    if not is_token_revoked(token, session):
        session.add(RevokedToken(token=token))
        session.commit()
