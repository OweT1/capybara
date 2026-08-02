"""Shared HTTP helpers with connection reuse and sane timeouts."""

from __future__ import annotations

import os
import threading

import requests
from loguru import logger

DEFAULT_TIMEOUT = 30

_thread_local = threading.local()


def get_session() -> requests.Session:
    """Return a thread-local requests.Session for connection pooling."""
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        _thread_local.session = session
    return session


def download_file(session: requests.Session, url: str, output_path: str) -> None:
    """Download ``url`` to ``output_path``, skipping if the file already exists."""
    if os.path.exists(output_path):
        logger.info(f"File already exists, skipping: {output_path}")
        return

    try:
        response = session.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Error reading url {url}: {e}"
        ) from e

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as file:
        file.write(response.content)
    logger.info(f"File has been downloaded at {output_path}")
