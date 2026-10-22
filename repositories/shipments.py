from sqlmodel import Session, select

from database.models import Shipment


def list_all(session: Session) -> list[Shipment]:
    return list(session.exec(select(Shipment)).all())


def get_by_id(shipment_id: int, session: Session) -> Shipment | None:
    return session.get(Shipment, shipment_id)


def add(shipment: Shipment, session: Session) -> Shipment:
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


def save(shipment: Shipment, session: Session) -> Shipment:
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


def remove(shipment: Shipment, session: Session) -> None:
    session.delete(shipment)
    session.commit()
