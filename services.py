from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from models import ParkingSlotModel

def create_parking_slot(db: Session, parking):
    try:
        new_slot = ParkingSlotModel(
            slot_code=parking.slot_code,
            zone_name=parking.zone_name,
            max_weight=parking.max_weight,
            is_available=parking.is_available
        )

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return new_slot

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

def get_all_slots(db: Session):
    return db.query(ParkingSlotModel).all()

def get_slot_by_id(db: Session, slot_id: int):

    slot = db.query(ParkingSlotModel).filter(
        ParkingSlotModel.id == slot_id
    ).first()

    if slot is None:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return slot