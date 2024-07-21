from time import sleep
from typing import Optional

import pyperclip
from loguru import logger

from utils.clipboard_sync_client import get_clipboard_sync_client, ClipboardSyncClient
from settings import settings


def _handle_clipboard_update(
        current_clipboard: str,
        previous_clipboard: str,
        sync_client: "ClipboardSyncClient",
        server_clipboard: str,
):
    """
        Defines if remote clipboard should replace current client's clipboard;
        returns appropriate clipboard
    """
    is_copied_different = current_clipboard != previous_clipboard

    if is_copied_different:
        logger.info(
            f"Client copied something new, sending to {settings.SYNC_SERVER_API_URL}"
        )
        sync_client.send(current_clipboard)
        return current_clipboard
    else:
        logger.info(
            f"Client received something new from {settings.SYNC_SERVER_API_URL}, copy..."
        )
        return server_clipboard


def _sync_cycle(
        sync_client: "ClipboardSyncClient", previous_clipboard: Optional[str]
) -> str:
    """returns current client's clipboard; sync it with remote clipboard"""
    server_clipboard = sync_client.retrieve()
    current_clipboard = pyperclip.paste()
    logger.debug(
        f"Clip '{server_clipboard}' received from {settings.SYNC_SERVER_API_URL}"
    )
    if server_clipboard != current_clipboard:
        # at this point this means that or client copied something new, and the clipboard on server should be updated
        # or client received new clipboard from server
        current_clipboard = _handle_clipboard_update(
            current_clipboard, previous_clipboard, sync_client, server_clipboard
        )

    current_clipboard_differ_from_previous = current_clipboard != previous_clipboard
    if current_clipboard_differ_from_previous:
        pyperclip.copy(current_clipboard)
    return current_clipboard


def sync_clipboard():
    previous_clipboard = None
    clipboard_sync_client = get_clipboard_sync_client()
    while True:
        previous_clipboard = _sync_cycle(clipboard_sync_client, previous_clipboard)
        sleep(settings.ITERATION_CYCLE_TIME)
