from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.routes.assistance.router import get_dispatcher
from app.routes.assistance.models import AssistanceRequest, ExternalError
from app.routes.assistance.models import RequestError

ENDPOINT = "/assistance"

REQUEST = {
    "topic": "Sales",
    "description": "I need help with my order #12345",
}


def test_unscoped_requests_will_fail(patch_token_scope):
    """
    This test simulate a request without the required scope getting a 403 response.
    """
    # arrange
    patch_token_scope()

    client = TestClient(app)

    # act
    response = client.post(
        ENDPOINT, json=REQUEST, headers={"Authorization": "Bearer test-token"}
    )

    # assert
    assert response.status_code == 403


def test_success(patch_token_scope, mocker):
    """
    This test simulate a successful request.
    """
    # arrange
    patch_token_scope("request-assistance")
    mocked_dispatcher = AsyncMock()
    app.dependency_overrides[get_dispatcher] = lambda: mocked_dispatcher
    client = TestClient(app)

    # act
    response = client.post(
        ENDPOINT, json=REQUEST, headers={"Authorization": "Bearer test-token"}
    )

    # assert
    assert response.status_code == 201
    mocked_dispatcher.notify.assert_called_once_with(
        AssistanceRequest(topic="Sales", description="I need help with my order #12345")
    )


def test_invalid_topic(patch_token_scope, mocker):
    """
    This test simulate a request with an invalid topic requested getting a 400 response and an error message.
    """
    # arrange
    patch_token_scope("request-assistance")
    mocked_dispatcher = AsyncMock()
    mocked_dispatcher.notify.side_effect = RequestError("Invalid topic")
    app.dependency_overrides[get_dispatcher] = lambda: mocked_dispatcher
    client = TestClient(app)

    # act
    response = client.post(
        ENDPOINT, json=REQUEST, headers={"Authorization": "Bearer test-token"}
    )

    # assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid topic"}


def test_external_error(patch_token_scope):
    """
    This test simulate a request that fails because of the underlying service
    returning an error and a 503 status.
    """
    # arrange
    patch_token_scope("request-assistance")
    mocked_dispatcher = AsyncMock()
    mocked_dispatcher.notify.side_effect = ExternalError(
        "Failed to send the notification"
    )
    app.dependency_overrides[get_dispatcher] = lambda: mocked_dispatcher
    client = TestClient(app)

    # act
    response = client.post(
        ENDPOINT, json=REQUEST, headers={"Authorization": "Bearer test-token"}
    )

    # assert
    assert response.status_code == 503
    assert response.json() == {"detail": "Failed to send the notification"}
