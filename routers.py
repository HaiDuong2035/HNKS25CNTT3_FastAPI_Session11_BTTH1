from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from schemas import ParkingSlotCreate
import services

router = APIRouter()

def response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/parking-slots", status_code=201)
def create_slot(
    parking: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    slot = services.create_parking_slot(db, parking)

    return response(
        201,
        "Thêm vị trí đỗ xe thành công",
        None,
        slot,
        request.url.path
    )

@router.get("/parking-slots")
def get_all(
    request: Request,
    db: Session = Depends(get_db)
):

    slots = services.get_all_slots(db)

    return response(
        200,
        "Success",
        None,
        slots,
        request.url.path
    )

@router.get("/parking-slots/{slot_id}")
def get_one(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    slot = services.get_slot_by_id(db, slot_id)

    return response(
        200,
        "Success",
        None,
        slot,
        request.url.path
    )