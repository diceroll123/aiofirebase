"""aiofirebase package."""
import asyncio
import functools
import json
import posixpath
from typing import Any, Callable, Dict, Literal, Optional, TypedDict

from aiohttp import ClientSession


class EventStreamPayload(TypedDict):
    path: str
    data: Any
    event: Literal["patch", "put"]
    stream_id: str


class StreamCancelled(Exception):
    """Signals the stream has been cancelled."""


class StreamAuthRevoked(Exception):
    """Signals the stream has been cancelled due to the authentication being revoked."""


class FirebaseHTTP:
    """
    HTTP Client for Firebase.

    Args:
        base_url (str): URL to your data.
        auth (string): Auth key.
        loop (class:`asyncio.BaseEventLoop`): Loop.
    """

    def __init__(
        self,
        base_url: str,
        auth: Optional[str] = None,
        loop: Optional[asyncio.BaseEventLoop] = None,
    ):
        """Initialise the class."""
        self._loop = loop or asyncio.get_event_loop()
        self._base_url = base_url
        self._auth = auth
        self._session = ClientSession(loop=self._loop)

    async def close(self):
        """Gracefully close the session."""
        await self._session.close()

    async def get(
        self, *, path: Optional[str] = None, params: Optional[Dict[str, Any]] = None
    ):
        """Perform a GET request."""
        return await self._request(method="GET", path=path, params=params)

    async def put(
        self,
        *,
        value: Any,
        path: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ):
        """Perform a put request."""
        return await self._request(method="PUT", value=value, path=path, params=params)

    async def post(
        self,
        *,
        value: Any,
        path: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ):
        """Perform a POST request."""
        return await self._request(method="POST", value=value, path=path, params=params)

    async def patch(
        self,
        *,
        value: Any,
        path: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ):
        """Perform a PATCH request."""
        return await self._request(
            method="PATCH", value=value, path=path, params=params
        )

    async def delete(
        self, *, path: Optional[str] = None, params: Optional[Dict[str, Any]] = None
    ):
        """Perform a DELETE request."""
        return await self._request(method="DELETE", path=path, params=params)

    async def stream(
        self,
        *,
        callback: Callable[[EventStreamPayload], None],
        path: Optional[str] = None,
        stream_id: Optional[str] = None
    ):
        """Hook up to the EventSource stream."""
        url = posixpath.join(self._base_url, path) if path else self._base_url
        url += ".json"
        headers = {"accept": "text/event-stream"}
        async with self._session.get(url, headers=headers, timeout=None) as resp:
            await FirebaseHTTP._iterate_over_stream(
                resp.content, callback, stream_id=stream_id or path
            )

    @staticmethod
    async def _iterate_over_stream(iterable, callback, stream_id):
        """Iterate over the EventSource stream and pass the event and data to the callback as and when we receive it."""
        event = None
        async for msg in iterable:
            msg_str = msg.decode("utf-8").strip()

            if not msg_str:
                continue

            key, value = msg_str.split(": ", 1)

            if key == "keep-alive":
                continue
            elif key == "event" and value == "cancel":
                raise StreamCancelled(
                    "The requested location is no longer allowed due to security/rules changes."
                )
            elif key == "event" and value == "auth_revoked":
                raise StreamAuthRevoked("The auth credentials has expired.")
            elif key == "event":
                event = value
            elif key == "data":
                data = json.loads(value)
                if data and event:
                    data["event"] = event
                    data["stream_id"] = stream_id
                    if asyncio.iscoroutinefunction(callback):
                        func = callback(data)
                    else:
                        func = asyncio.get_event_loop().run_in_executor(
                            None, functools.partial(callback, data)
                        )

                    asyncio.create_task(func)

    async def _request(self, *, method, value=None, path=None, params=None):
        """Perform a request to Firebase."""
        url = (
            posixpath.join(self._base_url, path.strip("/")) if path else self._base_url
        )
        url += ".json"
        data = json.dumps(value) if value else None
        async with self._session.request(method, url, data=data, params=params) as resp:
            assert resp.status == 200
            return await resp.json()
