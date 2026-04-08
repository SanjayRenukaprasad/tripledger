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

def test_register():
    res = client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    })
    assert res.status_code == 201
    assert res.json()["email"] == "test@test.com"

def test_register_duplicate_email():
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    })
    res = client.post("/auth/register", json={
        "name": "Test User 2",
        "email": "test@test.com",
        "password": "password123"
    })
    assert res.status_code == 400

def test_login():
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_invalid_credentials():
    res = client.post("/auth/login", data={
        "username": "wrong@test.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401