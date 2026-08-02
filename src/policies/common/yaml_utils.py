"""YAML load/save helpers."""

from __future__ import annotations

from typing import Any

import yaml
from loguru import logger


def load_yaml_file(file_name: str) -> Any:
    with open(file_name, "r") as f:
        return yaml.safe_load(f)


def save_dict_to_yaml_file(file_name: str, dict_item: dict) -> None:
    with open(file_name, "w") as output_file:
        yaml.dump(dict_item, output_file, sort_keys=False, default_flow_style=False)
    logger.info(f"File contents saved to {file_name}")
