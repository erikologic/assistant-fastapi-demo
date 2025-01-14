from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == 204

def test_unauthenticated_private_heartbeat_fail():
    response = client.get("/heartbeat/private")
    assert response.status_code == 403

def test_authenticated_private_heartbeat(mocker):
    mock_get_signing_key = mocker.patch("jwt.PyJWKClient.get_signing_key_from_jwt")
    mock_get_signing_key.return_value.key = "mock_signing_key"

    mock_decode = mocker.patch("jwt.decode")
    mock_decode.return_value = {"sub": "test_user"}
    
    response = client.get("/heartbeat/private", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 204