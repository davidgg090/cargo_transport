from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.database import Base, SQLALCHEMY_DATABASE_URL, SessionLocal, PackageDB, UserDB
from app.main import app

client = TestClient(app)

SQLALCHEMY_DATABASE_URL_TEST = SQLALCHEMY_DATABASE_URL.replace("test.db", "test_test.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    clear_mappers()


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()


def clean_db():
    db = SessionLocal()
    db.query(PackageDB).delete()
    db.query(UserDB).delete()
    db.commit()
    db.close()


@pytest.fixture
def token():
    clean_db()
    response = client.post("/auth/register/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    response = client.post("/auth/token/", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


def test_register_user(setup_database):
    clean_db()
    response = client.post("/auth/register/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_login_for_access_token(setup_database):
    clean_db()
    client.post("/auth/register/", json={"username": "testuser", "password": "testpass"})
    response = client.post("/auth/token/", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_add_package(setup_database, token):
    response = client.post("/cargo/packages/", json={
        "client": "Test Client",
        "weight": 10.0,
        "origin": "City A",
        "destination": "City B",
        "date": str(date.today())
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["client"] == "Test Client"
    assert "id" in data


def test_get_report(setup_database, token):
    clean_db()
    response = client.post("/auth/register/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    response = client.post("/auth/token/", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]

    client.post("/cargo/packages/", json={
        "client": "Test Client",
        "weight": 10.0,
        "origin": "City A",
        "destination": "City B",
        "date": str(date.today())
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get(f"/cargo/report/?report_date={str(date.today())}",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_packages"] == 1
    assert data["total_revenue"] == 10.0
