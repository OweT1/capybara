"""Path and naming helpers for scraped policy files."""

from __future__ import annotations

from pathlib import Path


def get_name_from_link(link: str) -> str:
    return Path(link).stem


def build_download_path(
    root: str, category: str, subcategory: str, policy: str, link: str
) -> str:
    return f"{root}/{category}/{subcategory}/{policy}/{get_name_from_link(link)}.pdf"
