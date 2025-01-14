import pytest


@pytest.fixture
def patch_token_scope(mocker):
    def _(scope=""):
        mock_get_signing_key = mocker.patch("jwt.PyJWKClient.get_signing_key_from_jwt")
        mock_get_signing_key.return_value.key = "mock_signing_key"

        mock_decode = mocker.patch("jwt.decode")
        mock_decode.return_value = {"scope": scope}

    yield _
