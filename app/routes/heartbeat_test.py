from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == 204


def test_unauthenticated_private_heartbeat_fail():
    response = client.get("/heartbeat/private")
    assert response.status_code == 403


def test_authenticated_private_heartbeat(patch_token_scope):
    patch_token_scope()

    response = client.get(
        "/heartbeat/private", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 204


def test_unscoped_heartbeat(patch_token_scope):
    patch_token_scope()

    response = client.get(
        "/heartbeat/scoped", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 403


def test_scoped_heartbeat(patch_token_scope):
    patch_token_scope("ping")
    response = client.get(
        "/heartbeat/scoped", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 204
