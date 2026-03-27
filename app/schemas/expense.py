from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ExpenseSplitCreate(BaseModel):
    user_id: int
    amount_owed: float

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    currency: str
    splits: Optional[List[ExpenseSplitCreate]] = None

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    currency: str
    amount_converted: Optional[float]
    category: Optional[str]
    paid_by: int
    trip_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AskBudgetRequest(BaseModel):
    question: str

class AskBudgetResponse(BaseModel):
    question: str
    answer: str