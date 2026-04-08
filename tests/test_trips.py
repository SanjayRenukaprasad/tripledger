import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def get_token():
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password123"
    })
    return res.json()["access_token"]

def test_create_trip():
    token = get_token()
    res = client.post("/trips", json={
        "name": "Japan 2026",
        "description": "Two weeks in Japan",
        "base_currency": "USD",
        "budget": 3000
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 201
    assert res.json()["name"] == "Japan 2026"
    assert res.json()["budget"] == 3000.0

def test_get_trips():
    token = get_token()
    client.post("/trips", json={
        "name": "Japan 2026",
        "base_currency": "USD",
        "budget": 3000
    }, headers={"Authorization": f"Bearer {token}"})
    res = client.get("/trips", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_trip_not_found():
    token = get_token()
    res = client.get("/trips/999", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404

def test_update_trip():
    token = get_token()
    create_res = client.post("/trips", json={
        "name": "Japan 2026",
        "base_currency": "USD",
        "budget": 3000
    }, headers={"Authorization": f"Bearer {token}"})
    trip_id = create_res.json()["id"]
    res = client.patch(f"/trips/{trip_id}", json={
        "budget": 5000
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["budget"] == 5000.0

def test_delete_trip():
    token = get_token()
    create_res = client.post("/trips", json={
        "name": "Japan 2026",
        "base_currency": "USD",
        "budget": 3000
    }, headers={"Authorization": f"Bearer {token}"})
    trip_id = create_res.json()["id"]
    res = client.delete(f"/trips/{trip_id}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204