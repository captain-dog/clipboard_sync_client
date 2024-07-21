import httpx


def get_httpx_client() -> httpx.Client:
    return httpx.Client()
