from fastapi.testclient import TestClient
from app.main import app
from app.routes.assistance import get_dispatcher
from app.routes.assistance.models import AssistanceRequest, ExternalError
from app.routes.assistance.models import RequestError

ENDPOINT = "/assistance"

REQUEST = {
    "topic": "Sales",
    "description": "I need help with my order #12345",
}


def test_success():
    # arrange
    class MockedDispatcher:
        def __init__(self):
            self.request = None

        async def notify(self, request):
            self.request = request

    mocked_dispatcher = MockedDispatcher()
    app.dependency_overrides[get_dispatcher] = lambda: mocked_dispatcher
    client = TestClient(app)

    # act
    response = client.post(ENDPOINT, json=REQUEST)

    # assert
    assert response.status_code == 201
    assert mocked_dispatcher.request == AssistanceRequest(
        topic="Sales", description="I need help with my order #12345"
    )


def test_invalid_topic():
    # arrange
    class MockedDispatcher:
        async def notify(self, request):
            raise RequestError("Invalid topic")

    mocked_dispatcher = MockedDispatcher()
    app.dependency_overrides[get_dispatcher] = lambda: mocked_dispatcher
    client = TestClient(app)

    # act
    response = client.post(ENDPOINT, json=REQUEST)

    # assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid topic"}


def test_external_error():
    # arrange
    class MockedDispatcher:
        async def notify(self, request):
            raise ExternalError("Failed to send the notification")

    mocked_dispatcher = MockedDispatcher()
    app.dependency_overrides[get_dispatcher] = lambda: mocked_dispatcher
    client = TestClient(app)

    # act
    response = client.post(ENDPOINT, json=REQUEST)

    # assert
    assert response.status_code == 503
    assert response.json() == {"detail": "Failed to send the notification"}
