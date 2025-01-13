from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_assistance_notification():
    notification_data = {
        "topic": "Sales",
        "description": "I need help with my order #12345"
    }
    
    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 201

# TODO test for invalid body