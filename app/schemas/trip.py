from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TripCreate(BaseModel):
    name: str
    description: Optional[str] = None
    base_currency: str = "USD"
    budget: float

class TripUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None

class TripResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    base_currency: str
    budget: float
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True