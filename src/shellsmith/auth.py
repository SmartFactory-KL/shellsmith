"""Sync and async auth."""

import time
import typing
from enum import Enum

import httpx
from httpx import Request, Response
from typing_extensions import override

from shellsmith.config import config


class GrantType(str, Enum):
    """Supported grant types."""

    CLIENT_CREDENTIALS = "client_credentials"
    PASSWORD = "password"

    def __str__(self) -> str:
        """Return the enum member's value as its string representation."""
        return self.value


class TokenProvider:
    """Base class for token providers.

    To implement a custom token provider scheme, subclass `TokenProvider`
    and add data elements in self._data.
    """

    def __init__(
        self,
        token_url: str,
        grant_type: GrantType,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize a token provider.

        Args:
            token_url: URL of the token endpoint.
            grant_type: Grant type used to obtain the token.
            timeout: Request timeout in seconds.
        """
        self._token_url = token_url
        self._grant_type = grant_type
        self._timeout = timeout

        self._token = None
        self._expires_at = 0

        self._data = {"grant_type": self._grant_type}

    def _token_valid(self) -> bool:
        """Return whether the current token exists and has not expired."""
        return self._token and time.time() < self._expires_at

    def _save_token(self, payload: dict[str, typing.Any]) -> None:
        """Save the access token and calculate its expiration time.

        Args:
            payload: Token response containing ``access_token`` and optionally
                ``expires_in`` in seconds.
        """
        self._token = payload["access_token"]
        self._expires_at = time.time() + payload.get("expires_in", 3600)

    def get_token_sync(self) -> str:
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

    async def get_token_async(self) -> str:
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
    """Token provider using password."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize a password token provider.

        Args:
            token_url: URL of the token endpoint.
            client_id: Client identifier.
            client_secret: Client secret.
            username: Username.
            password: Password.
            timeout: Request timeout in seconds.
        """
        super().__init__(
            token_url=token_url, timeout=timeout, grant_type=GrantType.PASSWORD
        )

        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password

        self._data.update(
            {
                "username": self._username,
                "password": self._password,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            }
        )


class ClientCredentialsTokenProvider(TokenProvider):
    """Token provider using client credentials."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize a client credentials token provider.

        Args:
            token_url: URL of the token endpoint.
            client_id: Client identifier.
            client_secret: Client secret.
            timeout: Request timeout in seconds.
        """
        super().__init__(
            token_url=token_url,
            timeout=timeout,
            grant_type=GrantType.CLIENT_CREDENTIALS,
        )
        self._client_id = client_id
        self._client_secret = client_secret

        self._data.update(
            {
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            }
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
        token = self.token_provider.get_token_sync()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    @override
    async def async_auth_flow(
        self, request: Request
    ) -> typing.Generator[Request, Response, None]:
        """Asynchronously fetch a token and add it to the request header."""
        token = await self.token_provider.get_token_async()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request
