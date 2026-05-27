"""User settings persistence for interactive mode."""

import configparser
import logging
from pathlib import Path
from typing import Any

from src.config import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

CONFIG_PATH = Path.home() / ".sorting_visualizer.ini"


def load_settings() -> dict[str, Any]:
    """Load settings from user config file or return defaults."""
    config = configparser.ConfigParser()
    if not CONFIG_PATH.exists():
        return dict(DEFAULT_SETTINGS)

    try:
        config.read(CONFIG_PATH)
        settings: dict[str, Any] = {}
        for key, default in DEFAULT_SETTINGS.items():
            if config.has_option("DEFAULT", key):
                raw = config.get("DEFAULT", key)
                if isinstance(default, int):
                    settings[key] = int(raw)
                elif isinstance(default, float):
                    settings[key] = float(raw)
                else:
                    settings[key] = raw
            else:
                settings[key] = default
        return settings
    except Exception:
        logger.warning("Corrupted config file, using defaults.", exc_info=True)
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict[str, Any]) -> None:
    """Save settings dict to ~/.sorting_visualizer.ini."""
    config = configparser.ConfigParser()
    config["DEFAULT"] = {k: str(v) for k, v in settings.items()}
    with open(CONFIG_PATH, "w") as f:
        config.write(f)
    logger.info("Settings saved to %s", CONFIG_PATH)
