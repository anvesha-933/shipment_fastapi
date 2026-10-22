from schemas import Ship, ShipmentStatus, UpdateShipment


shipments = {
    1270: {"weight": 12.5, "content": "wooden table", "status": "delivered"},
    1271: {"weight": 13.5, "content": "toys", "status": "pending"},
    1272: {"weight": 10.2, "content": "chair", "status": "shipped"},
    1273: {"weight": 5.1, "content": "books", "status": "pending"},
    1274: {"weight": 22.0, "content": "refrigerator", "status": "delivered"},
    1275: {"weight": 3.7, "content": "clothes", "status": "shipped"},
    1276: {"weight": 8.9, "content": "shoes", "status": "pending"},
    1277: {"weight": 15.0, "content": "monitor", "status": "delivered"},
    1278: {"weight": 6.3, "content": "keyboard", "status": "shipped"},
    1279: {"weight": 1.1, "content": "mouse", "status": "pending"},
}


def all_shipments():
    return shipments


def has_shipments() -> bool:
    return bool(shipments)


def has_shipment(shipment_id: int) -> bool:
    return shipment_id in shipments


def latest_shipment():
    shipment_id = max(shipments)
    return {"id": shipment_id, **shipments[shipment_id]}


def shipment_by_id(shipment_id: int):
    return shipments[shipment_id]


def create_raw_shipment(weight: float, content: str):
    shipment_id = max(shipments.keys(), default=1000) + 1
    shipments[shipment_id] = {
        "weight": weight,
        "content": content,
        "status": "placed",
    }
    return {"id": shipment_id, **shipments[shipment_id]}


def create_schema_shipment(data: Ship):
    shipment_id = max(shipments.keys(), default=1000) + 1
    shipment = {
        "id": shipment_id,
        "weight": data.weight,
        "content": data.content,
        "status": (
            data.status.value
            if hasattr(data.status, "value")
            else str(data.status)
        ),
    }
    shipments[shipment_id] = shipment
    return shipment


def update_shipment(shipment_id: int, weight: float, content: str):
    shipments[shipment_id].update({"weight": weight, "content": content})
    return shipments[shipment_id]


def replace_shipment(shipment_id: int, data: UpdateShipment):
    shipments[shipment_id] = {
        "id": shipment_id,
        "weight": data.weight,
        "content": data.content,
        "status": ShipmentStatus.shipped.value,
    }
    return shipments[shipment_id]


def remove_shipment(shipment_id: int) -> None:
    shipments.pop(shipment_id)
