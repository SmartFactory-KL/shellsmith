"""Sync and async auth."""

import time
import typing
from dataclasses import dataclass

import httpx
from httpx import Request, Response
from typing_extensions import override

from shellsmith.config import config


@dataclass
class UserAuthentication:
    """Authentication data for user-based authentication.

    Args:
        username: Username used for authentication.
        password: Password used for authentication.
    """

    username: str
    password: str


@dataclass
class ClientAuthentication:
    """Authentication data for client-based authentication.

    Args:
        client_id: The unique identifier of the client used for authentication.
        client_secret: The secret associated with the client used for authentication.
    """

    client_id: str
    client_secret: str


class TokenProvider:
    """Base class for token providers.

    To implement a custom token provider scheme, subclass `TokenProvider`
    and provide data.
    """

    def __init__(
        self,
        token_url: str,
        data: dict[str, str],
        timeout: float = config.timeout,
    ) -> None:
        """Initialize a token provider.

        Args:
            token_url: URL of the token endpoint.
            data: Data required to request an access token,
                including the grant type and authentication credentials.
            timeout: Request timeout in seconds.
        """
        self._token_url = token_url
        self._timeout = timeout

        self._token = None
        self._expires_at = 0

        self._data = data

    def _token_valid(self) -> bool:
        """Return whether the current token exists and has not expired."""
        return self._token and time.time() < self._expires_at

    def _save_token(self, data: dict[str, typing.Any]) -> None:
        """Save the access token and calculate its expiration time.

        Args:
            data: Token response containing ``access_token`` and optionally
                ``expires_in`` in seconds.
        """
        self._token = data["access_token"]
        self._expires_at = time.time() + data.get("expires_in", 3600)

    def sync_get_token(self) -> str:
        """Return a valid access token synchronously, refreshing it when necessary."""
        if self._token_valid():
            return self._token

        with httpx.Client() as client:
            response = client.post(
                self._token_url, timeout=self._timeout, data=self._data
            )
            response.raise_for_status()
            self._save_token(response.json())

        return self._token

    async def async_get_token(self) -> str:
        """Return a valid access token asynchronously, refreshing it when necessary."""
        if self._token_valid():
            return self._token

        async with httpx.AsyncClient() as client:
            r = await client.post(
                self._token_url, timeout=self._timeout, data=self._data
            )
            r.raise_for_status()
            payload = r.json()

        self._save_token(payload)
        return self._token


class PasswordTokenProvider(TokenProvider):
    """Token provider using password grant type (see https://www.rfc-editor.org/info/rfc6749/#section-4.3)."""

    def __init__(
        self,
        token_url: str,
        user_authentication: UserAuthentication,
        client_authentication: ClientAuthentication | None = None,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize a password token provider.

        Args:
            token_url: URL of the token endpoint.
            user_authentication: Username and password.
            client_authentication: Optional client identifier and client secret.
            timeout: Request timeout in seconds.
        """
        _data = {
            "username": user_authentication.username,
            "password": user_authentication.password,
            "grant_type": "password",
        }

        if client_authentication:
            _data.update(
                {
                    "client_id": client_authentication.client_id,
                    "client_secret": client_authentication.client_secret,
                }
            )

        super().__init__(token_url=token_url, data=_data, timeout=timeout)


class ClientCredentialsTokenProvider(TokenProvider):
    """Token provider using client credentials grant type (see https://www.rfc-editor.org/info/rfc6749/#section-2.3)."""

    def __init__(
        self,
        token_url: str,
        client_authentication: ClientAuthentication,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize a client credentials token provider.

        Args:
            token_url: URL of the token endpoint.
            client_authentication: Client identifier and client secret.
            timeout: Request timeout in seconds.
        """
        super().__init__(
            token_url=token_url,
            data={
                "client_id": client_authentication.client_id,
                "client_secret": client_authentication.client_secret,
                "grant_type": "client_credentials",
            },
            timeout=timeout,
        )


class Auth(httpx.Auth):
    """Authentication handler that adds an access token to httpx.request."""

    def __init__(self, token_provider: "TokenProvider") -> None:
        """Initialize the authentication handler.

        Args:
            token_provider: Provider used to obtain an access token.
        """
        self.token_provider = token_provider

    @override
    def sync_auth_flow(
        self, request: Request
    ) -> typing.Generator[Request, Response, None]:
        """Synchronously fetch a token and add it to the request header."""
        token = self.token_provider.sync_get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    @override
    async def async_auth_flow(
        self, request: Request
    ) -> typing.Generator[Request, Response, None]:
        """Asynchronously fetch a token and add it to the request header."""
        token = await self.token_provider.async_get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request
