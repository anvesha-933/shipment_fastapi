from fastapi import APIRouter, Body, HTTPException, status

from schemas import Response, Ship, UpdateShipment
from services import fundamentals


router = APIRouter()


@router.get("/shipments")
def get_all_shipments():
    return fundamentals.all_shipments()


@router.get("/shipments/latest")
def get_latest_shipment():
    if not fundamentals.has_shipments():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shipments available",
        )
    return fundamentals.latest_shipment()


@router.get("/shipments/{shipment_id}")
def get_shipment_by_id(shipment_id: int):
    if not fundamentals.has_shipment(shipment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment with that id not found",
        )
    return fundamentals.shipment_by_id(shipment_id)


@router.get("/shipments/verify/{shipment_id}")
def get_by_id_weight(shipment_id: int, weight: float):
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight should be greater than 0",
        )
    if not fundamentals.has_shipment(shipment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment with that id not found",
        )
    shipment = fundamentals.shipment_by_id(shipment_id)
    if shipment["weight"] != weight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight does not match records",
        )
    return shipment


@router.post("/shipments/raw")
def create_shipment_raw(weight: float = Body(...), content: str = Body(...)):
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be greater than zero",
        )
    return fundamentals.create_raw_shipment(weight, content)


@router.post("/new-ship", response_model=Response)
def create_shipment_schema(data: Ship):
    return fundamentals.create_schema_shipment(data)


@router.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int, weight: float, content: str):
    if not fundamentals.has_shipment(shipment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    shipment = fundamentals.update_shipment(shipment_id, weight, content)
    return {
        "message": f"Shipment #{shipment_id} updated successfully",
        "shipment": shipment,
    }


@router.put("/update-shipment/{shipment_id}")
def update_shipment_with_schema(shipment_id: int, data: UpdateShipment):
    if not fundamentals.has_shipment(shipment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    return fundamentals.replace_shipment(shipment_id, data)


@router.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int):
    if shipment_id not in fundamentals.shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    fundamentals.remove_shipment(shipment_id)
    return {"message": f"Shipment #{shipment_id} deleted successfully"}
