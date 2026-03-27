from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, trips, expenses, members, ai

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TripLedger API",
    description="AI-powered travel budget tracking API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(trips.router)
app.include_router(expenses.router)
app.include_router(members.router)
app.include_router(ai.router)

@app.get("/health")
def health():
    return {"status": "ok"}