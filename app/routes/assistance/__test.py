import pytest
from app.routes.assistance import channels
from fastapi.testclient import TestClient
from app.main import app
from app.routes.assistance.models import Notification


class InMemoryChannel:
    def __init__(self):
        self.notifications = []

    def send(self, notification: Notification):
        self.notifications.append(notification)


class FailingChannel:
    def send(self, notification: Notification):
        raise Exception("The underlying API request failed")


@pytest.fixture
def mocked_channels():
    return {
        "Sales": InMemoryChannel(),
        "Pricing": InMemoryChannel(),
        "Failing": FailingChannel(),
    }


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


def test_failed_notification(client, mocked_channels):
    notification_data = {
        "topic": "Failing",
        "description": "I need help so much!",
    }
    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 503
    assert response.json() == {"detail": "Failed to send the notification"}
