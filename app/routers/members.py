from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trip import Trip
from app.models.member import TripMember
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/trips/{trip_id}/members", tags=["members"])

@router.post("/{user_id}", status_code=201)
def add_member(trip_id: int, user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    existing = db.query(TripMember).filter(
        TripMember.trip_id == trip_id,
        TripMember.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already a member")
    member = TripMember(trip_id=trip_id, user_id=user_id)
    db.add(member)
    db.commit()
    return {"message": "Member added successfully"}

@router.delete("/{user_id}", status_code=204)
def remove_member(trip_id: int, user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    member = db.query(TripMember).filter(
        TripMember.trip_id == trip_id,
        TripMember.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()