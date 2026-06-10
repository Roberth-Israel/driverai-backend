from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "DriverAI Pro"


def test_login_invalid_credentials():
    response = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "wrong",
    })
    assert response.status_code == 401


def test_register():
    response = client.post("/api/v1/auth/register", json={
        "name": "Test Driver",
        "email": "test@driverai.com",
        "password": "test123456",
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["name"] == "Test Driver"
