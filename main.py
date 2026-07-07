from fastapi import FastAPI, Depends, status, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from service import create_parking_slot, get_all_db, search_slot_by_id
from typing import Optional, Any
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class ParkingSlotBase(BaseModel):
    slot_code: str
    zone_name: str = Field(min_length=3)
    max_weight: int = Field(gt=0)
    is_available: bool

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any]
    errors: Optional[Any]
    time_stamp: str
    path: str

def create_response(sc, mess, req: Request, data = None, er = None):
    return BaseResponse(
        status_code = sc,
        message = mess,
        data = data,
        errors = er,
        time_stamp = datetime.now().isoformat(),
        path = req.url.path
    )

@app.post('/parking-slots')
def post_parking_slot(
    new_parking_slot: ParkingSlotBase,
    req: Request,
    db: Session = Depends(get_db)
):
    new_parking_slot = create_parking_slot(db, new_parking_slot.slot_code, new_parking_slot.zone_name, new_parking_slot.max_weight, new_parking_slot.is_available)
    if new_parking_slot:
        return create_response(
            status.HTTP_201_CREATED,
            'Create Success!',
            req,
            {
                'id': new_parking_slot.id,
                'slot_code': new_parking_slot.slot_code,
                'zone_name': new_parking_slot.zone_name,
                'max_weight': new_parking_slot.max_weight,
                'is_available': new_parking_slot.is_available
            }
        )
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        'Create Failed!'
    )

@app.get('/parking-slots')
def get_parking_slots(
    req: Request,
    db: Session = Depends(get_db)
):
    return create_response(
        status.HTTP_200_OK,
        'Display Success!',
        req,
        get_all_db(db)
    )

@app.get('/parking-slots/{slot_id}')
def get_parking_slot(
    slot_id: int,
    req: Request,
    db: Session = Depends(get_db)
):
    slot = search_slot_by_id(db, slot_id)
    if slot:
        return create_response(
            status.HTTP_200_OK,
            'Search Success!',
            req,
            slot
        )
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        'Slot Not Found!'
    )

@app.exception_handler(HTTPException)
def http_exception_handle(req: Request, exc: HTTPException):
    response = create_response(exc.status_code, 'HTTP Error!', req, er = exc.detail)
    return JSONResponse(response.model_dump(), exc.status_code)

@app.exception_handler(Exception)
def global_exception_handle(req: Request, exc: Exception):
    response = create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Server Error!', req, er = str(exc))
    return JSONResponse(response.model_dump(), status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(RequestValidationError)
def validation_exception_handle(req: Request, exc: RequestValidationError):
    response = create_response(status.HTTP_422_UNPROCESSABLE_CONTENT, 'Validation Error!', req, er = str(exc))
    return JSONResponse(response.model_dump(), status.HTTP_422_UNPROCESSABLE_CONTENT)