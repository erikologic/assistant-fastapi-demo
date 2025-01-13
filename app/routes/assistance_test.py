from app.routes.assistance import AssistanceRequest, Channel, get_channel_resolver
from fastapi.testclient import TestClient
from app.main import app


class InMemoryChannel(Channel):
    def __init__(self):
        self.notifications = []

    def send(self, notification: AssistanceRequest):
        self.notifications.append(notification)


class InMemoryChannelResolver:
    def __init__(self):
        self.channels = {}

    def add(self, topic: str, channel: Channel):
        self.channels[topic] = channel

    def get(self, topic: str) -> Channel:
        return self.channels[topic]


def test_create_assistance_notification():
    sales = InMemoryChannel()
    channel_resolver = InMemoryChannelResolver()
    channel_resolver.add("Sales", sales)
    app.dependency_overrides[get_channel_resolver] = lambda: channel_resolver
    client = TestClient(app)

    notification_data = {
        "topic": "Sales",
        "description": "I need help with my order #12345",
    }

    response = client.post("/assistance", json=notification_data)
    assert response.status_code == 201
    assert sales.notifications == [
        AssistanceRequest(description="I need help with my order #12345")
    ]


# TODO test for invalid body
