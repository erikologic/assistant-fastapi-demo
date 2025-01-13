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


def test_create_sales_assistance_notification():
    mocked_channels = {"Sales": InMemoryChannel()}
    app.dependency_overrides[channels] = lambda: mocked_channels
    client = TestClient(app)

    notification_data = {
        "topic": "Sales",
        "description": "I need help with my order #12345",
    }

    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 201
    assert mocked_channels["Sales"].notifications == [
        Notification(description="I need help with my order #12345")
    ]


def test_create_pricing_assistance_notification():
    mocked_channels = {
        "Sales": InMemoryChannel(),
        "Pricing": InMemoryChannel(),
    }
    app.dependency_overrides[channels] = lambda: mocked_channels
    client = TestClient(app)

    notification_data = {
        "topic": "Pricing",
        "description": "What's the price for the product #12345?",
    }

    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 201
    assert mocked_channels["Pricing"].notifications == [
        Notification(description="What's the price for the product #12345?")
    ]


# TODO test for invalid body
