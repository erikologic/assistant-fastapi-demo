from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == 204
