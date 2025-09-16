"""Sync and async client classes for AAS operations."""

import mimetypes
from pathlib import Path
from types import TracebackType
from typing import Any
from urllib.parse import quote

import httpx
from httpx import Response

from shellsmith.config import config
from shellsmith.types import JSON
from shellsmith.utils import base64_encoded


class AsyncClient:
    """Async client for AAS operations using httpx."""

    def __init__(
        self,
        host: str = config.host,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize async client.

        Args:
            host: Base URL of the AAS server. Defaults to configured host.
            timeout: Request timeout in seconds.
        """
        self.host = host
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "AsyncClient":
        """Enter async context manager."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(
        self,
        exc_type: BaseException | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Ensure client is initialized."""
        if not self._client or self._client.is_closed:
            raise RuntimeError(
                "Client not initialized or closed. Use async with statement."
            )
        return self._client

    async def _request(
        self, method: str, path: str, json: Any | None = None, **kwargs: Any
    ) -> Response:
        url = f"{self.host}{path}"
        timeout = kwargs.get("timeout", self.timeout)
        response = await self.client.request(
            method=method,
            url=url,
            timeout=timeout,
            json=json,
            **kwargs,
        )
        response.raise_for_status()
        return response

    # ─────────────────────────────────── Shells ───────────────────────────────────────

    async def get_shells(self) -> dict:
        """Retrieves all Shells from the AAS server.

        Corresponds to:
        GET /shells

        Returns:
            A list of dictionaries representing the Shells.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        path = "/shells"
        response = await self._request(method=method, path=path)
        json_response = response.json()
        return json_response

    async def get_shell(self, shell_id: str, encode: bool = True) -> dict:
        """Retrieves a specific Shell by its ID.

        Corresponds to:
        GET /shells/{shell_id}

        Args:
            shell_id: The unique identifier of the Shell.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Returns:
            A dictionary representing the Shell.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}"
        response = await self._request(method=method, path=path)
        return response.json()

    async def create_shell(self, shell: dict) -> dict:
        """Creates a new Shell on the AAS server.

        Corresponds to:
        POST /shells

        Args:
            shell: A dictionary representing the Shell to be created.

        Returns:
            A dictionary representing the created Shell.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        path = "/shells"
        response = await self._request(method=method, path=path, json=shell)
        return response.json()

    async def update_shell(
        self, shell_id: str, shell: dict, encode: bool = True
    ) -> None:
        """Updates an existing Shell on the AAS server by its ID.

        Corresponds to:
        PUT /shells/{shell_id}

        Args:
            shell_id: The unique identifier of the Shell.
            shell: A dictionary representing the updated Shell content.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Raises:
            HTTPError: If the PUT request fails.
        """
        method = "PUT"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}"
        await self._request(method=method, path=path, json=shell)

    async def delete_shell(self, shell_id: str, encode: bool = True) -> None:
        """Deletes a specific Shell by its ID.

        Corresponds to:
        DELETE /shells/{shell_id}

        Args:
            shell_id: The unique identifier of the Shell.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}"
        await self._request(method=method, path=path)

    async def get_submodel_refs(
        self,
        shell_id: str,
        encode: bool = True,
        **kwargs: Any,
    ) -> dict:
        """Retrieves all submodel references from a specific Shell.

        Corresponds to:
        GET /shells/{shell_id}/submodel-refs

        Args:
            shell_id: The unique identifier of the Shell.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            A list of dictionaries representing the submodel references.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}/submodel-refs"
        response = await self._request(method=method, path=path, **kwargs)
        return response.json()

    async def create_submodel_ref(
        self,
        shell_id: str,
        submodel_ref: dict,
        encode: bool = True,
    ) -> None:
        """Creates a submodel reference for a specific Shell.

        Corresponds to:
        POST /shells/{shell_id}/submodel-refs

        Args:
            shell_id: The unique identifier of the Shell.
            submodel_ref: A dictionary representing the submodel reference to be added.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}/submodel-refs"
        await self._request(method=method, path=path, json=submodel_ref)

    async def delete_submodel_ref(
        self,
        shell_id: str,
        submodel_id: str,
        encode: bool = True,
    ) -> None:
        """Deletes a specific submodel reference from a Shell.

        Corresponds to:
        DELETE /shells/{shell_id}/submodel-refs/{submodel_id}

        Args:
            shell_id: The unique identifier of the Shell.
            submodel_id: The unique identifier of the submodel.
            encode: Whether to Base64-encode both identifiers. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        shell_id = base64_encoded(shell_id, encode)
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/shells/{shell_id}/submodel-refs/{submodel_id}"
        await self._request(method=method, path=path)

    # ───────────────────────────────── Submodels ──────────────────────────────────────

    async def get_submodels(self) -> dict:
        """Retrieves all Submodels from the AAS server.

        Corresponds to:
        GET /submodels

        Returns:
            A list of dictionaries representing the Submodels.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        path = "/submodels"
        response = await self._request(method=method, path=path)
        return response.json()

    async def get_submodel(self, submodel_id: str, encode: bool = True) -> dict:
        """Retrieves a specific Submodel by its ID.

        Corresponds to:
        GET /submodels/{submodel_id}

        Args:
            submodel_id: The unique identifier of the submodel.
            encode: Whether to Base64-encode the submodel ID. Defaults to True.

        Returns:
            A dictionary representing the submodel.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}"
        response = await self._request(method=method, path=path)
        return response.json()

    async def create_submodel(self, submodel: dict) -> dict:
        """Creates a new Submodel on the AAS server.

        Corresponds to:
        POST /submodels

        Args:
            submodel: A dictionary representing the Submodel to be created.

        Returns:
            A dictionary representing the created Submodel.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        path = "/submodels"
        response = await self._request(method=method, path=path, json=submodel)
        return response.json()

    async def update_submodel(
        self,
        submodel_id: str,
        submodel: dict,
        encode: bool = True,
    ) -> None:
        """Updates an existing Submodel by its ID.

        Corresponds to:
        PUT /submodels/{submodel_id}

        Args:
            submodel_id: The unique identifier of the Submodel.
            submodel: A dictionary representing the updated Submodel content.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PUT request fails.
        """
        method = "PUT"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}"
        await self._request(method=method, path=path, json=submodel)

    async def delete_submodel(self, submodel_id: str, encode: bool = True) -> None:
        """Deletes a specific Submodel by its ID.

        Corresponds to:
        DELETE /submodels/{submodel_id}

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}"
        await self._request(method=method, path=path)

    async def get_submodel_value(
        self,
        submodel_id: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves the raw value of a specific Submodel.

        Corresponds to:
        GET /submodels/{submodel_id}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the Submodel value.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/$value"
        response = await self._request(method=method, path=path)
        return response.json()

    async def update_submodel_value(
        self,
        submodel_id: str,
        value: list[dict],
        encode: bool = True,
    ) -> None:
        """Updates the value of a specific Submodel.

        Corresponds to:
        PATCH /submodels/{submodel_id}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            value: A list[dict] of SubmodelElements with updated values.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PATCH request fails.
        """
        method = "PATCH"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/$value"
        await self._request(method=method, path=path, json=value)

    async def get_submodel_metadata(
        self,
        submodel_id: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves the metadata of a specific Submodel.

        Corresponds to:
        GET /submodels/{submodel_id}/$metadata

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the Submodel metadata.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/$metadata"
        response = await self._request(method=method, path=path)
        return response.json()

    # ───────────────────────────── Submodel Elements ──────────────────────────────────

    async def get_submodel_elements(
        self,
        submodel_id: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves all Submodel elements from a specific Submodel.

        Corresponds to:
        GET /submodels/{submodel_id}/submodel-elements

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A list of dictionaries representing the Submodel elements.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/submodel-elements"

        response = await self._request(method=method, path=path)
        return response.json()

    async def create_submodel_element(
        self,
        submodel_id: str,
        element: dict,
        id_short_path: str | None = None,
        encode: bool = True,
    ) -> None:
        """Creates a Submodel element.

        If `id_short_path` is given, creates the element at that nested path.
        Otherwise, creates the element at the root level.

        Corresponds to:
        POST /submodels/{submodel_id}/submodel-elements
        POST /submodels/{submodel_id}/submodel-elements/{idShortPath}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path for the new Submodel element.
            element: A dictionary representing the Submodel element to create.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        submodel_id = base64_encoded(submodel_id, encode)
        base = f"/submodels/{submodel_id}/submodel-elements"
        path = f"{base}/{quote(id_short_path, safe='')}" if id_short_path else base
        await self._request(method=method, path=path, json=element)

    async def get_submodel_element(
        self,
        submodel_id: str,
        id_short_path: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves a specific Submodel element by its idShort path.

        Corresponds to:
        GET /submodels/{submodel_id}/submodel-elements/{id_short_path}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the submodel element.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}"

        response = await self._request(method=method, path=path)
        return response.json()

    async def update_submodel_element(
        self,
        submodel_id: str,
        id_short_path: str,
        element: dict,
        encode: bool = True,
    ) -> None:
        """Updates or creates a Submodel element by full replacement.

        Corresponds to:
        PUT /submodels/{submodel_id}/submodel-elements/{idShortPath}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            element: A dictionary representing the new element content.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PUT request fails.
        """
        method = "PUT"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}"
        await self._request(method=method, path=path, json=element)

    async def delete_submodel_element(
        self,
        submodel_id: str,
        id_short_path: str,
        encode: bool = True,
    ) -> None:
        """Deletes a specific Submodel element by its idShort path.

        Corresponds to:
        DELETE /submodels/{submodel_id}/submodel-elements/{idShortPath}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")

        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}"
        await self._request(method=method, path=path)

    async def get_submodel_element_value(
        self,
        submodel_id: str,
        id_short_path: str,
        encode: bool = True,
    ) -> JSON:
        """Retrieves the raw value of a specific Submodel element.

        Corresponds to:
        GET /submodels/{submodel_id}/submodel-elements/{idShortPath}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the raw value.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}/$value"
        response = await self._request(method=method, path=path)
        return response.json()

    async def update_submodel_element_value(
        self,
        submodel_id: str,
        id_short_path: str,
        value: str,
        encode: bool = True,
    ) -> None:
        """Updates the value of a specific Submodel element.

        Corresponds to:
        PATCH /submodels/{submodel_id}/submodel-elements/{id_short_path}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            value: The new value to assign to the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PATCH request fails.
        """
        method = "PATCH"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}/$value"
        await self._request(method=method, path=path, json=value)

    async def get_health_status(self, **kwargs: Any) -> str:
        """Check health status of the AAS environment."""
        method = "GET"
        path = "/actuator/health"
        try:
            response = await self._request(method=method, path=path, **kwargs)
            data = response.json()
            return data["status"]
        except httpx.RequestError:
            return "DOWN"

    async def is_healthy(self, **kwargs: Any) -> bool:
        """Check if the AAS environment is ready for requests."""
        return await self.get_health_status(**kwargs) == "UP"

    # ───────────────────────────────── Upload ─────────────────────────────────────────

    async def upload_aas(self, path: Path | str) -> bool:
        """Uploads a single AAS file to the configured server.

        Acceptable formats: `.json`, `.xml`, `.aasx`.

        Args:
            path: The path to the AAS file. Can be a `Path` or string.

        Returns:
            True if the upload succeeds, otherwise False.
        """
        path = Path(path)
        endpoint = "/upload"

        mime_type, _ = mimetypes.guess_type(path)  # .json, .xml
        if mime_type is None:
            # .aasx
            mime_type = "application/octet-stream"

        with open(path, "rb") as file:
            files = [("file", (path.name, file, mime_type))]
            try:
                response = await self._request(
                    method="POST", path=endpoint, files=files
                )
                success: bool = response.json()
                print(f"✅ Successfully uploaded '{path.name}': {success}")
                return success
            except httpx.HTTPStatusError as e:
                print(f"❌ Failed to upload '{path.name}': {e}")
                return False

    async def upload_aas_folder(self, path: Path | str) -> None:
        """Uploads all AAS files from a specified folder.

        Accepts `.json`, `.xml`, and `.aasx` files only.

        Args:
            path: The path to the folder containing AAS files.

        Raises:
            ValueError: If the provided path is not a valid directory.
        """
        folder_path = Path(path)

        if not folder_path.is_dir():
            raise ValueError(f"{folder_path} is not a valid directory.")

        for aas_file in folder_path.iterdir():
            if aas_file.is_file() and aas_file.suffix in {".json", ".xml", ".aasx"}:
                print(f"Uploading: '{aas_file.name}'")
                await self.upload_aas(aas_file)


class Client:
    """Sync client for AAS operations using httpx."""

    def __init__(
        self,
        host: str = config.host,
        timeout: float = config.timeout,
    ) -> None:
        """Initialize sync client.

        Args:
            host: Base URL of the AAS server. Defaults to configured host.
            timeout: Request timeout in seconds.
        """
        self.host = host
        self.timeout = timeout
        self._client: httpx.Client | None = None

    def __enter__(self) -> "Client":
        """Enter context manager."""
        self._client = httpx.Client(timeout=self.timeout)
        return self

    def __exit__(
        self,
        exc_type: BaseException | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        if self._client:
            self._client.close()

    @property
    def client(self) -> httpx.Client:
        """Ensure client is initialized."""
        if not self._client or self._client.is_closed:
            raise RuntimeError("Client not initialized or closed. Use with statement.")
        return self._client

    def _request(
        self,
        method: str,
        path: str,
        json: Any | None = None,
        **kwargs: Any,
    ) -> Response:
        url = f"{self.host}{path}"
        timeout = kwargs.get("timeout", self.timeout)
        response = self.client.request(
            method=method,
            url=url,
            timeout=timeout,
            json=json,
            **kwargs,
        )
        response.raise_for_status()
        return response

    # ─────────────────────────────────── Shells ───────────────────────────────────────

    def get_shells(self) -> dict:
        """Retrieves all Shells from the AAS server.

        Corresponds to:
        GET /shells

        Returns:
            A list of dictionaries representing the Shells.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        path = "/shells"
        response = self._request(method=method, path=path)
        json_response = response.json()
        return json_response

    def get_shell(self, shell_id: str, encode: bool = True) -> dict:
        """Retrieves a specific Shell by its ID.

        Corresponds to:
        GET /shells/{shell_id}

        Args:
            shell_id: The unique identifier of the Shell.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Returns:
            A dictionary representing the Shell.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}"
        response = self._request(method=method, path=path)
        return response.json()

    def create_shell(self, shell: dict) -> dict:
        """Creates a new Shell on the AAS server.

        Corresponds to:
        POST /shells

        Args:
            shell: A dictionary representing the Shell to be created.

        Returns:
            A dictionary representing the created Shell.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        path = "/shells"
        response = self._request(method=method, path=path, json=shell)
        return response.json()

    def update_shell(self, shell_id: str, shell: dict, encode: bool = True) -> None:
        """Updates an existing Shell on the AAS server by its ID.

        Corresponds to:
        PUT /shells/{shell_id}

        Args:
            shell_id: The unique identifier of the Shell.
            shell: A dictionary representing the updated Shell content.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Raises:
            HTTPError: If the PUT request fails.
        """
        method = "PUT"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}"
        self._request(method=method, path=path, json=shell)

    def delete_shell(self, shell_id: str, encode: bool = True) -> None:
        """Deletes a specific Shell by its ID.

        Corresponds to:
        DELETE /shells/{shell_id}

        Args:
            shell_id: The unique identifier of the Shell.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}"
        self._request(method=method, path=path)

    def get_submodel_refs(
        self,
        shell_id: str,
        encode: bool = True,
        **kwargs: Any,
    ) -> dict:
        """Retrieves all submodel references from a specific Shell.

        Corresponds to:
        GET /shells/{shell_id}/submodel-refs

        Args:
            shell_id: The unique identifier of the Shell.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            A list of dictionaries representing the submodel references.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}/submodel-refs"
        response = self._request(method=method, path=path, **kwargs)
        return response.json()

    def create_submodel_ref(
        self,
        shell_id: str,
        submodel_ref: dict,
        encode: bool = True,
    ) -> None:
        """Creates a submodel reference for a specific Shell.

        Corresponds to:
        POST /shells/{shell_id}/submodel-refs

        Args:
            shell_id: The unique identifier of the Shell.
            submodel_ref: A dictionary representing the submodel reference to be added.
            encode: Whether to Base64-encode the Shell ID. Defaults to True.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        shell_id = base64_encoded(shell_id, encode)
        path = f"/shells/{shell_id}/submodel-refs"
        self._request(method=method, path=path, json=submodel_ref)

    def delete_submodel_ref(
        self,
        shell_id: str,
        submodel_id: str,
        encode: bool = True,
    ) -> None:
        """Deletes a specific submodel reference from a Shell.

        Corresponds to:
        DELETE /shells/{shell_id}/submodel-refs/{submodel_id}

        Args:
            shell_id: The unique identifier of the Shell.
            submodel_id: The unique identifier of the submodel.
            encode: Whether to Base64-encode both identifiers. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        shell_id = base64_encoded(shell_id, encode)
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/shells/{shell_id}/submodel-refs/{submodel_id}"
        self._request(method=method, path=path)

    # ───────────────────────────────── Submodels ──────────────────────────────────────

    def get_submodels(self) -> dict:
        """Retrieves all Submodels from the AAS server.

        Corresponds to:
        GET /submodels

        Returns:
            A list of dictionaries representing the Submodels.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        path = "/submodels"
        response = self._request(method=method, path=path)
        return response.json()

    def get_submodel(self, submodel_id: str, encode: bool = True) -> dict:
        """Retrieves a specific Submodel by its ID.

        Corresponds to:
        GET /submodels/{submodel_id}

        Args:
            submodel_id: The unique identifier of the submodel.
            encode: Whether to Base64-encode the submodel ID. Defaults to True.

        Returns:
            A dictionary representing the submodel.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}"
        response = self._request(method=method, path=path)
        return response.json()

    def create_submodel(self, submodel: dict) -> dict:
        """Creates a new Submodel on the AAS server.

        Corresponds to:
        POST /submodels

        Args:
            submodel: A dictionary representing the Submodel to be created.

        Returns:
            A dictionary representing the created Submodel.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        path = "/submodels"
        response = self._request(method=method, path=path, json=submodel)
        return response.json()

    def update_submodel(
        self,
        submodel_id: str,
        submodel: dict,
        encode: bool = True,
    ) -> None:
        """Updates an existing Submodel by its ID.

        Corresponds to:
        PUT /submodels/{submodel_id}

        Args:
            submodel_id: The unique identifier of the Submodel.
            submodel: A dictionary representing the updated Submodel content.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PUT request fails.
        """
        method = "PUT"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}"
        self._request(method=method, path=path, json=submodel)

    def delete_submodel(self, submodel_id: str, encode: bool = True) -> None:
        """Deletes a specific Submodel by its ID.

        Corresponds to:
        DELETE /submodels/{submodel_id}

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}"
        self._request(method=method, path=path)

    def get_submodel_value(
        self,
        submodel_id: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves the raw value of a specific Submodel.

        Corresponds to:
        GET /submodels/{submodel_id}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the Submodel value.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/$value"
        response = self._request(method=method, path=path)
        return response.json()

    def update_submodel_value(
        self,
        submodel_id: str,
        value: list[dict],
        encode: bool = True,
    ) -> None:
        """Updates the value of a specific Submodel.

        Corresponds to:
        PATCH /submodels/{submodel_id}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            value: A list[dict] of SubmodelElements with updated values.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PATCH request fails.
        """
        method = "PATCH"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/$value"
        self._request(method=method, path=path, json=value)

    def get_submodel_metadata(
        self,
        submodel_id: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves the metadata of a specific Submodel.

        Corresponds to:
        GET /submodels/{submodel_id}/$metadata

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the Submodel metadata.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/$metadata"
        response = self._request(method=method, path=path)
        return response.json()

    # ───────────────────────────── Submodel Elements ──────────────────────────────────

    def get_submodel_elements(
        self,
        submodel_id: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves all Submodel elements from a specific Submodel.

        Corresponds to:
        GET /submodels/{submodel_id}/submodel-elements

        Args:
            submodel_id: The unique identifier of the Submodel.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A list of dictionaries representing the Submodel elements.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        path = f"/submodels/{submodel_id}/submodel-elements"

        response = self._request(method=method, path=path)
        return response.json()

    def create_submodel_element(
        self,
        submodel_id: str,
        element: dict,
        id_short_path: str | None = None,
        encode: bool = True,
    ) -> None:
        """Creates a Submodel element.

        If `id_short_path` is given, creates the element at that nested path.
        Otherwise, creates the element at the root level.

        Corresponds to:
        POST /submodels/{submodel_id}/submodel-elements
        POST /submodels/{submodel_id}/submodel-elements/{idShortPath}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path for the new Submodel element.
            element: A dictionary representing the Submodel element to create.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the POST request fails.
        """
        method = "POST"
        submodel_id = base64_encoded(submodel_id, encode)
        base = f"/submodels/{submodel_id}/submodel-elements"
        path = f"{base}/{quote(id_short_path, safe='')}" if id_short_path else base
        self._request(method=method, path=path, json=element)

    def get_submodel_element(
        self,
        submodel_id: str,
        id_short_path: str,
        encode: bool = True,
    ) -> dict:
        """Retrieves a specific Submodel element by its idShort path.

        Corresponds to:
        GET /submodels/{submodel_id}/submodel-elements/{id_short_path}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the submodel element.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}"

        response = self._request(method=method, path=path)
        return response.json()

    def update_submodel_element(
        self,
        submodel_id: str,
        id_short_path: str,
        element: dict,
        encode: bool = True,
    ) -> None:
        """Updates or creates a Submodel element by full replacement.

        Corresponds to:
        PUT /submodels/{submodel_id}/submodel-elements/{idShortPath}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            element: A dictionary representing the new element content.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PUT request fails.
        """
        method = "PUT"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}"
        self._request(method=method, path=path, json=element)

    def delete_submodel_element(
        self,
        submodel_id: str,
        id_short_path: str,
        encode: bool = True,
    ) -> None:
        """Deletes a specific Submodel element by its idShort path.

        Corresponds to:
        DELETE /submodels/{submodel_id}/submodel-elements/{idShortPath}

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the DELETE request fails.
        """
        method = "DELETE"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")

        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}"
        self._request(method=method, path=path)

    def get_submodel_element_value(
        self,
        submodel_id: str,
        id_short_path: str,
        encode: bool = True,
    ) -> JSON:
        """Retrieves the raw value of a specific Submodel element.

        Corresponds to:
        GET /submodels/{submodel_id}/submodel-elements/{idShortPath}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Returns:
            A dictionary representing the raw value.

        Raises:
            HTTPError: If the GET request fails.
        """
        method = "GET"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}/$value"
        response = self._request(method=method, path=path)
        return response.json()

    def update_submodel_element_value(
        self,
        submodel_id: str,
        id_short_path: str,
        value: str,
        encode: bool = True,
    ) -> None:
        """Updates the value of a specific Submodel element.

        Corresponds to:
        PATCH /submodels/{submodel_id}/submodel-elements/{id_short_path}/$value

        Args:
            submodel_id: The unique identifier of the Submodel.
            id_short_path: The idShort path of the Submodel element.
            value: The new value to assign to the Submodel element.
            encode: Whether to Base64-encode the Submodel ID. Defaults to True.

        Raises:
            HTTPError: If the PATCH request fails.
        """
        method = "PATCH"
        submodel_id = base64_encoded(submodel_id, encode)
        encoded_path = quote(id_short_path, safe="")
        path = f"/submodels/{submodel_id}/submodel-elements/{encoded_path}/$value"
        self._request(method=method, path=path, json=value)

    def get_health_status(self, **kwargs: Any) -> str:
        """Check health status of the AAS environment.

        Args:
            **kwargs: Additional keyword arguments to pass to the request.
        """
        method = "GET"
        path = "/actuator/health"
        try:
            response = self._request(method=method, path=path, **kwargs)
            data = response.json()
            return data["status"]
        except httpx.RequestError:
            return "DOWN"

    def is_healthy(self, **kwargs: Any) -> bool:
        """Check if the AAS environment is ready for requests.

        Args:
            **kwargs: Additional keyword arguments to pass to the request.
        """
        return self.get_health_status(**kwargs) == "UP"

    # ───────────────────────────────── Upload ─────────────────────────────────────────

    def upload_aas(self, path: Path | str) -> bool:
        """Uploads a single AAS file to the configured server.

        Acceptable formats: `.json`, `.xml`, `.aasx`.

        Args:
            path: The path to the AAS file. Can be a `Path` or string.

        Returns:
            True if the upload succeeds, otherwise False.
        """
        path = Path(path)
        endpoint = "/upload"

        mime_type, _ = mimetypes.guess_type(path)  # .json, .xml
        if mime_type is None:
            # .aasx
            mime_type = "application/octet-stream"

        with open(path, "rb") as file:
            files = [("file", (path.name, file, mime_type))]
            try:
                response = self._request(method="POST", path=endpoint, files=files)
                success: bool = response.json()
                print(f"✅ Successfully uploaded '{path.name}': {success}")
                return success
            except httpx.HTTPStatusError as e:
                print(f"❌ Failed to upload '{path.name}': {e}")
                return False

    def upload_aas_folder(self, path: Path | str) -> None:
        """Uploads all AAS files from a specified folder.

        Accepts `.json`, `.xml`, and `.aasx` files only.

        Args:
            path: The path to the folder containing AAS files.

        Raises:
            ValueError: If the provided path is not a valid directory.
        """
        folder_path = Path(path)

        if not folder_path.is_dir():
            raise ValueError(f"{folder_path} is not a valid directory.")

        for aas_file in folder_path.iterdir():
            if aas_file.is_file() and aas_file.suffix in {".json", ".xml", ".aasx"}:
                print(f"Uploading: '{aas_file.name}'")
                self.upload_aas(aas_file)
