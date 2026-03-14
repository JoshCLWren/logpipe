"""Logger setup with rotating file and console handlers."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logger(
    name: str | None = None,
    level: LogLevel = "INFO",
    log_file: Path | str | None = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    log_format: str | None = None,
    date_format: str | None = None,
    console: bool = True,
    force: bool = False,
) -> logging.Logger:
    """Set up a logger with rotating file and console handlers.

    Args:
        name: Logger name. If None, returns the root logger.
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file. If None, no file handler is created.
        max_bytes: Maximum size of each log file in bytes (default: 10MB).
        backup_count: Number of backup files to keep (default: 5).
        log_format: Custom log format string.
        date_format: Custom date format string.
        console: Whether to add a console handler (default: True).
        force: If True, clear existing handlers before reconfiguring (default: False).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    if logger.handlers and not force:
        return logger

    if force and logger.handlers:
        logger.handlers.clear()

    logger.setLevel(getattr(logging, level))

    default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    default_date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(
        fmt=log_format or default_format,
        datefmt=date_format or default_date_format,
    )

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Get an existing logger without reconfiguring handlers.

    Args:
        name: Logger name. If None, returns the root logger.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
