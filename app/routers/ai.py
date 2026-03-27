from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import AskBudgetRequest, AskBudgetResponse
from app.routers.auth import get_current_user
from app.services.ai import ask_budget_question
from app.services.debt import simplify_debts, get_trip_splits
from collections import defaultdict

router = APIRouter(prefix="/trips/{trip_id}", tags=["ai"])

@router.post("/ask", response_model=AskBudgetResponse)
async def ask_budget(
    trip_id: int,
    req: AskBudgetRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    expenses = db.query(Expense).filter(Expense.trip_id == trip_id).all()

    total_spent = sum(e.amount_converted or 0 for e in expenses)
    breakdown = defaultdict(float)
    for e in expenses:
        breakdown[e.category or "other"] += e.amount_converted or 0

    trip_data = {
        "name": trip.name,
        "base_currency": trip.base_currency,
        "budget": trip.budget,
        "total_spent": total_spent,
        "breakdown": dict(breakdown)
    }

    answer = await ask_budget_question(trip_data, req.question)
    return {"question": req.question, "answer": answer}

@router.get("/settle")
def get_settlement(
    trip_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.owner_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    splits = get_trip_splits(db, trip_id)
    if not splits:
        return {"transactions": [], "message": "No unsettled expenses"}

    transactions = simplify_debts(splits)
    return {"transactions": transactions}