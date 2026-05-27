"""Global configuration for the sorting visualizer."""

import logging
from pathlib import Path

# Maximum allowed array size for visualization performance.
MAX_ARRAY_SIZE: int = 512

# Visualization settings
INACTIVE_COLOR: str = "#B0B0B0"  # neutral gray for default columns

# Logging
LOG_DIR: Path = Path("logs")
LOG_LEVEL: int = logging.INFO
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Default values for user settings (used by config_io)
DEFAULT_SETTINGS: dict[str, object] = {
    "last_algorithm": "bubble",
    "array_size": 32,
    "speed_interval": 50,
    "log_level": "INFO",
}
