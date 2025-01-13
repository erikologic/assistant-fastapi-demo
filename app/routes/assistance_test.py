import pytest
from app.routes.assistance import (
    Notification,
    Channel,
    channels,
)
from fastapi.testclient import TestClient
from app.main import app


class InMemoryChannel(Channel):
    def __init__(self):
        self.notifications = []

    def send(self, notification: Notification):
        self.notifications.append(notification)


@pytest.fixture
def mocked_channels():
    return {"Sales": InMemoryChannel(), "Pricing": InMemoryChannel()}


@pytest.fixture
def client(mocked_channels):
    app.dependency_overrides[channels] = lambda: mocked_channels
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_sales_assistance_notification(client, mocked_channels):
    notification_data = {
        "topic": "Sales",
        "description": "I need help with my order #12345",
    }

    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 201
    assert mocked_channels["Sales"].notifications == [
        Notification(description="I need help with my order #12345")
    ]


def test_create_pricing_assistance_notification(client, mocked_channels):
    notification_data = {
        "topic": "Pricing",
        "description": "What's the price for the product #12345?",
    }

    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 201
    assert mocked_channels["Pricing"].notifications == [
        Notification(description="What's the price for the product #12345?")
    ]


def test_create_assistance_notification_invalid_topic(client):
    notification_data = {
        "topic": "Invalid",
        "description": "I need help with my order #12345",
    }
    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid topic"}
