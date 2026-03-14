"""Convenience logging functions using a root logger."""

from __future__ import annotations

import logging
from typing import Any

_root_logger: logging.Logger | None = None


def configure_root_logger(
    level: str = "INFO",
    log_file: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    log_format: str | None = None,
    date_format: str | None = None,
    console: bool = True,
    force: bool = False,
) -> logging.Logger:
    """Configure the root logger used by convenience functions.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file. If None, no file handler is created.
        max_bytes: Maximum size of each log file in bytes (default: 10MB).
        backup_count: Number of backup files to keep (default: 5).
        log_format: Custom log format string.
        date_format: Custom date format string.
        console: Whether to add a console handler (default: True).
        force: If True, clear existing handlers before reconfiguring (default: False).

    Returns:
        Configured root logger instance.
    """
    global _root_logger

    from .logger import setup_logger

    _root_logger = setup_logger(
        name=None,
        level=level,  # type: ignore[arg-type]
        log_file=log_file,
        max_bytes=max_bytes,
        backup_count=backup_count,
        log_format=log_format,
        date_format=date_format,
        console=console,
        force=force,
    )

    return _root_logger


def _get_root_logger() -> logging.Logger:
    """Get the root logger, creating a basic one if needed."""
    global _root_logger

    if _root_logger is None:
        _root_logger = logging.getLogger()
        if not _root_logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            _root_logger.addHandler(handler)
            _root_logger.setLevel(logging.INFO)

    return _root_logger


# Convenience functions use Any for **kwargs to match logging module signatures
def debug(msg: str, *args: Any, **kwargs: Any) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN401
    """Log a debug message using the root logger."""
    _get_root_logger().debug(msg, *args, **kwargs)


def info(msg: str, *args: Any, **kwargs: Any) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN401
    """Log an info message using the root logger."""
    _get_root_logger().info(msg, *args, **kwargs)


def warning(msg: str, *args: Any, **kwargs: Any) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN401
    """Log a warning message using the root logger."""
    _get_root_logger().warning(msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs: Any) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN401
    """Log an error message using the root logger."""
    _get_root_logger().error(msg, *args, **kwargs)


def critical(msg: str, *args: Any, **kwargs: Any) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN401
    """Log a critical message using the root logger."""
    _get_root_logger().critical(msg, *args, **kwargs)
