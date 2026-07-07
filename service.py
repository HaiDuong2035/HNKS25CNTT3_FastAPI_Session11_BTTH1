from sqlalchemy.orm import Session
from models import ParkingSlotModel
from fastapi.encoders import jsonable_encoder

def create_parking_slot(db: Session, slot_code: str, zone_name: str, max_weight: int, is_available = None):
    try:
        new_parking_slot = ParkingSlotModel(
            slot_code = slot_code,
            zone_name = zone_name,
            max_weight = max_weight,
            is_available = is_available
        )
        db.add(new_parking_slot)
        db.commit()
        db.refresh(new_parking_slot)
        return new_parking_slot
    except:
        db.rollback()
        return None

def get_all_db(db: Session):
    return jsonable_encoder(db.query(ParkingSlotModel).all())

def search_slot_by_id(db: Session, slot_id: int):
    slot_list = jsonable_encoder(db.query(ParkingSlotModel).all())
    for slot in slot_list:
        if slot['id'] == slot_id:
            return slot
    return None