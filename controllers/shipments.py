from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database.models import Shipment
from database.sessions import get_session
from schemas import Ship, ShipmentPatch
from services.exceptions import ShipmentNotFound
from services.shipments import (
    create_shipment,
    delete_shipment,
    get_shipment,
    list_shipments,
    patch_shipment,
    replace_shipment,
)


router = APIRouter()


def _not_found_error(shipment_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Shipment #{shipment_id} not found",
    )


@router.post(
    "/new-shipment",
    response_model=Shipment,
    status_code=status.HTTP_201_CREATED,
)
def add_shipment(data: Ship, session: Session = Depends(get_session)):
    return create_shipment(data, session)


@router.get("/shipments", response_model=list[Shipment])
def get_all_shipments(session: Session = Depends(get_session)):
    return list_shipments(session)


@router.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment_by_id(shipment_id: int, session: Session = Depends(get_session)):
    try:
        return get_shipment(shipment_id, session)
    except ShipmentNotFound:
        raise _not_found_error(shipment_id)


@router.put("/shipments/{shipment_id}", response_model=Shipment)
def update_shipment(
    shipment_id: int, data: Ship, session: Session = Depends(get_session)
):
    try:
        return replace_shipment(shipment_id, data, session)
    except ShipmentNotFound:
        raise _not_found_error(shipment_id)


@router.patch("/shipments/{shipment_id}", response_model=Shipment)
def update_shipment_partial(
    shipment_id: int,
    data: ShipmentPatch,
    session: Session = Depends(get_session),
):
    try:
        return patch_shipment(shipment_id, data, session)
    except ShipmentNotFound:
        raise _not_found_error(shipment_id)


@router.delete("/shipments/{shipment_id}")
def remove_shipment(shipment_id: int, session: Session = Depends(get_session)):
    try:
        delete_shipment(shipment_id, session)
    except ShipmentNotFound:
        raise _not_found_error(shipment_id)
    return {"message": f"Shipment #{shipment_id} deleted successfully"}
