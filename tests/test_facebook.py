import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, FacebookAccount, MetricSnapshot
from app.auth.utils import get_password_hash
from app.auth.dependencies import create_access_token

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


@pytest.fixture
def test_user_and_token():
    """Create a test user and return auth token."""
    db = TestingSessionLocal()
    user = User(email="test@example.com", hashed_password=get_password_hash("testpass123"))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": user.id})
    db.close()
    return {"user": user, "token": token}


def test_oauth_login_generates_url(test_user_and_token):
    """Test that OAuth login endpoint generates authorization URL."""
    token = test_user_and_token["token"]
    response = client.get(
        "/facebook/oauth/login",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "authorization_url" in data
    assert "facebook.com" in data["authorization_url"]
    assert "client_id" in data["authorization_url"]


def test_insert_system_user_token(test_user_and_token):
    """Test inserting a system user token."""
    token = test_user_and_token["token"]
    response = client.post(
        "/facebook/system_user/token",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "ad_account_id": "act_123456789",
            "access_token": "test_system_token_12345",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["ad_account_id"] == "act_123456789"
    assert data["is_system_user"] is True
    assert data["expires_at"] is None


def test_list_facebook_accounts(test_user_and_token):
    """Test listing Facebook accounts."""
    user = test_user_and_token["user"]
    token = test_user_and_token["token"]

    # Create a test Facebook account
    db = TestingSessionLocal()
    fb_account = FacebookAccount(
        user_id=user.id,
        ad_account_id="act_123456789",
        access_token="test_token",
        token_type="Bearer",
        expires_at=datetime.utcnow() + timedelta(days=60),
        is_system_user=False,
    )
    db.add(fb_account)
    db.commit()
    db.close()

    # List accounts
    response = client.get(
        "/facebook/accounts",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ad_account_id"] == "act_123456789"


def test_get_insights_from_db(test_user_and_token):
    """Test retrieving insights from database."""
    user = test_user_and_token["user"]
    token = test_user_and_token["token"]

    # Setup: Create FB account and metrics
    db = TestingSessionLocal()
    fb_account = FacebookAccount(
        user_id=user.id,
        ad_account_id="act_123456789",
        access_token="test_token",
        token_type="Bearer",
        is_system_user=False,
    )
    db.add(fb_account)
    db.commit()
    db.refresh(fb_account)

    # Add test metrics
    metric = MetricSnapshot(
        facebook_account_id=fb_account.id,
        ts=datetime.utcnow().date(),
        level="campaign",
        entity_id="camp_123",
        impressions=1000,
        clicks=50,
        spend=100.0,
        conversions=5,
        revenue=500.0,
    )
    db.add(metric)
    db.commit()
    db.close()

    # Query insights
    response = client.get(
        "/facebook/act/act_123456789/insights_from_db?limit=10&page=1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["impressions"] == 1000
    assert data["items"][0]["ctr"] == 5.0  # (50/1000)*100
    assert data["items"][0]["roas"] == 5.0  # 500/100


def test_get_insights_unauthorized_account(test_user_and_token):
    """Test accessing insights for account not owned by user."""
    token = test_user_and_token["token"]

    response = client.get(
        "/facebook/act/act_999999999/insights_from_db",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_oauth_login_requires_auth():
    """Test that OAuth endpoints require authentication."""
    response = client.get("/facebook/oauth/login")
    assert response.status_code == 401