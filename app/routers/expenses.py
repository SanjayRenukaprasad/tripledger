from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.member import ExpenseSplit
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.routers.auth import get_current_user
from typing import List

router = APIRouter(prefix="/trips/{trip_id}/expenses", tags=["expenses"])

def get_trip_or_404(trip_id: int, user: User, db: Session):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("", response_model=ExpenseResponse, status_code=201)
async def add_expense(trip_id: int, req: ExpenseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    trip = get_trip_or_404(trip_id, user, db)

    # Convert currency
    from app.services.currency import convert_amount
    amount_converted = await convert_amount(req.amount, req.currency, trip.base_currency)

    # AI categorization
    from app.services.ai import categorize_expense
    category = await categorize_expense(req.description)

    expense = Expense(
        description=req.description,
        amount=req.amount,
        currency=req.currency,
        amount_converted=amount_converted,
        category=category,
        paid_by=user.id,
        trip_id=trip.id
    )
    db.add(expense)
    db.flush()

    if req.splits:
        for s in req.splits:
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=s.user_id,
                amount_owed=s.amount_owed
            )
            db.add(split)

    db.commit()
    db.refresh(expense)
    return expense

@router.get("", response_model=List[ExpenseResponse])
def get_expenses(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    get_trip_or_404(trip_id, user, db)
    return db.query(Expense).filter(Expense.trip_id == trip_id).all()

@router.delete("/{expense_id}", status_code=204)
def delete_expense(trip_id: int, expense_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    get_trip_or_404(trip_id, user, db)
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.trip_id == trip_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()