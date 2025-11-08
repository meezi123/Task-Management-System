import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
from auth import get_current_user
# SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def override_get_current_user():
    return "test_user"

app.dependency_overrides[get_current_user] = override_get_current_user

# Fixture for TestClient
@pytest.fixture()
def client():
    # Create tables for each test session
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)
