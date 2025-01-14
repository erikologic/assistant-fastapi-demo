from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


@pytest.fixture
def patch_verify_token(mocker):
    def _(scope=""):
        mock_get_signing_key = mocker.patch("jwt.PyJWKClient.get_signing_key_from_jwt")
        mock_get_signing_key.return_value.key = "mock_signing_key"

        mock_decode = mocker.patch("jwt.decode")
        mock_decode.return_value = {"scope": scope}

    yield _


def test_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == 204


def test_unauthenticated_private_heartbeat_fail():
    response = client.get("/heartbeat/private")
    assert response.status_code == 403


def test_authenticated_private_heartbeat(patch_verify_token):
    patch_verify_token()

    response = client.get(
        "/heartbeat/private", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 204


def test_unscoped_heartbeat(patch_verify_token):
    patch_verify_token()

    response = client.get(
        "/heartbeat/scoped", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 403


def test_scoped_heartbeat(patch_verify_token):
    patch_verify_token("ping")
    response = client.get(
        "/heartbeat/scoped", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 204
