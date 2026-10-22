from sqlmodel import Session

from database.models import Shipment
from repositories import shipments as shipment_repository
from schemas import Ship, ShipmentPatch
from services.exceptions import ShipmentNotFound


def create_shipment(data: Ship, session: Session) -> Shipment:
    shipment = Shipment.model_validate(data.model_dump())
    return shipment_repository.add(shipment, session)


def list_shipments(session: Session) -> list[Shipment]:
    return shipment_repository.list_all(session)


def get_shipment(shipment_id: int, session: Session) -> Shipment:
    shipment = shipment_repository.get_by_id(shipment_id, session)
    if shipment is None:
        raise ShipmentNotFound()
    return shipment


def replace_shipment(shipment_id: int, data: Ship, session: Session) -> Shipment:
    shipment = get_shipment(shipment_id, session)
    shipment.sqlmodel_update(data.model_dump())
    return shipment_repository.save(shipment, session)


def patch_shipment(
    shipment_id: int, data: ShipmentPatch, session: Session
) -> Shipment:
    shipment = get_shipment(shipment_id, session)
    shipment.sqlmodel_update(data.model_dump(exclude_unset=True))
    return shipment_repository.save(shipment, session)


def delete_shipment(shipment_id: int, session: Session) -> None:
    shipment = get_shipment(shipment_id, session)
    shipment_repository.remove(shipment, session)
