"""Logger setup with rotating file handlers and convenience functions."""

from __future__ import annotations

from logpipe.convenience import (
    configure_root_logger,
    critical,
    debug,
    error,
    info,
    warning,
)
from logpipe.logger import LogLevel, get_logger, setup_logger

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "LogLevel",
    "setup_logger",
    "get_logger",
    "configure_root_logger",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
]
