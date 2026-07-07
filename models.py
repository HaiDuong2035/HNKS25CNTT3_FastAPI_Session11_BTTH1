from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from database import engine
from pydantic import Field

Base = declarative_base()

class ParkingSlotModel(Base):
    __tablename__ = 'parking_slots'
    id = Column(Integer, primary_key=True)
    slot_code = Column(String(50), nullable=False, unique=True)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=1)

Base.metadata.create_all(bind=engine)