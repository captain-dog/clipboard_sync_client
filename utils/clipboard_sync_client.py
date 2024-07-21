from urllib.parse import urljoin

import httpx

from settings import settings
from utils.httpx_client import get_httpx_client


class ClipboardSyncClient:
    _endpoint: str = "clip"

    def __init__(self, client: httpx.Client, channel: str, url: str) -> None:
        self._httpx_client = client
        self._channel = channel
        self._url = url

    def retrieve(self) -> str | None:
        url = urljoin(self._url, self._endpoint)
        headers = {"user": self._channel}
        req = httpx.Request(url=url, headers=headers, method="GET")
        response = self._httpx_client.send(req)
        return response.json().get("clip")

    def send(self, message: str) -> None:
        url = urljoin(self._url, self._endpoint)
        headers = {"user": self._channel}
        req = httpx.Request(
            url=url, headers=headers, method="POST", json={"message": message}
        )
        self._httpx_client.send(req)
        return None


def get_clipboard_sync_client() -> ClipboardSyncClient:
    return ClipboardSyncClient(
        client=get_httpx_client(),
        channel=settings.CHANNEL,
        url=settings.SYNC_SERVER_API_URL,
    )
