from unittest.mock import Mock, patch

from shellsmith.auth import (
    ClientAuthentication,
    ClientCredentialsTokenProvider,
    PasswordTokenProvider,
    TokenProvider,
    UserAuthentication,
)


def verify_provider(token_provider: TokenProvider):
    now = 0
    expires: int = 5

    response = Mock()
    response.json.return_value = {
        "access_token": "test-token",
        "expires_in": expires,
    }

    with patch("httpx.Client.post", return_value=response):
        token = token_provider.sync_get_token()

    assert token == "test-token"
    token_provider._expires_at = now + expires

    with patch("shellsmith.auth.time.time", return_value=now):
        assert token_provider._token_valid()

    with patch("shellsmith.auth.time.time", return_value=now + expires + 1):
        assert not token_provider._token_valid()


def test_client_credentials_provider():

    client_credentials_provider = ClientCredentialsTokenProvider(
        token_url="token_url",
        client_authentication=ClientAuthentication(
            client_id="client_id", client_secret="client_secret"
        ),
    )

    verify_provider(client_credentials_provider)


def test_password_provider():

    password_provider = PasswordTokenProvider(
        token_url="token_url",
        user_authentication=UserAuthentication(
            username="username", password="password"
        ),
        client_authentication=ClientAuthentication(
            client_id="client_id", client_secret="client_secret"
        ),
    )

    verify_provider(password_provider)
