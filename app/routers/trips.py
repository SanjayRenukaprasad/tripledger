from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import TripCreate, TripUpdate, TripResponse
from app.routers.auth import get_current_user
from typing import List

router = APIRouter(prefix="/trips", tags=["trips"])

@router.post("", response_model=TripResponse, status_code=201)
def create_trip(req: TripCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = Trip(**req.dict(), owner_id=user.id)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

@router.get("", response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Trip).filter(Trip.owner_id == user.id).all()

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.patch("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, req: TripUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    for key, val in req.dict(exclude_none=True).items():
        setattr(trip, key, val)
    db.commit()
    db.refresh(trip)
    return trip

@router.delete("/{trip_id}", status_code=204)
def delete_trip(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()