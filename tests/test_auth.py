import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth.utils import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email():
    """Test registration with duplicate email."""
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "different123"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success():
    """Test successful login."""
    # Register user first
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123"},
    )

    # Login
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    """Test login with wrong password."""
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user():
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401