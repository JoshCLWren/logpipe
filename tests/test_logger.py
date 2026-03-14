"""Tests for logpipe logger setup."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest

from logpipe import (
    critical,
    debug,
    error,
    get_logger,
    info,
    setup_logger,
    warning,
)
from logpipe.convenience import configure_root_logger
from logpipe.logger import LogLevel


class TestSetupLogger:
    """Tests for setup_logger function."""

    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        logger = setup_logger("test_basic", level="INFO")
        assert logger.name == "test_basic"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_setup_logger_with_debug_level(self):
        """Test logger with DEBUG level."""
        logger = setup_logger("test_debug", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logger_with_warning_level(self):
        """Test logger with WARNING level."""
        logger = setup_logger("test_warning", level="WARNING")
        assert logger.level == logging.WARNING

    def test_setup_logger_with_error_level(self):
        """Test logger with ERROR level."""
        logger = setup_logger("test_error", level="ERROR")
        assert logger.level == logging.ERROR

    def test_setup_logger_with_critical_level(self):
        """Test logger with CRITICAL level."""
        logger = setup_logger("test_critical", level="CRITICAL")
        assert logger.level == logging.CRITICAL

    def test_setup_logger_no_console(self):
        """Test logger without console handler."""
        logger = setup_logger("test_no_console", level="INFO", console=False)
        assert len(logger.handlers) == 0

    def test_setup_logger_with_file(self, tmp_path: Path):
        """Test logger with file handler."""
        log_file = tmp_path / "test.log"
        logger = setup_logger("test_file", level="INFO", log_file=log_file, console=False)
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], RotatingFileHandler)

    def test_setup_logger_file_rotation(self, tmp_path: Path):
        """Test logger with custom file rotation settings."""
        log_file = tmp_path / "rotation.log"
        logger = setup_logger(
            "test_rotation",
            level="DEBUG",
            log_file=log_file,
            max_bytes=1024,
            backup_count=3,
            console=False,
        )
        handler = logger.handlers[0]
        assert isinstance(handler, RotatingFileHandler)
        assert handler.maxBytes == 1024
        assert handler.backupCount == 3

    def test_setup_logger_custom_format(self):
        """Test logger with custom format."""
        custom_format = "%(levelname)s: %(message)s"
        logger = setup_logger("test_format", level="INFO", log_format=custom_format)
        handler = logger.handlers[0]
        assert handler.formatter is not None
        assert handler.formatter._fmt == custom_format  # noqa: SLF001

    def test_setup_logger_returns_same_logger(self):
        """Test that calling setup_logger twice returns same logger."""
        logger1 = setup_logger("test_same", level="INFO")
        logger2 = setup_logger("test_same", level="DEBUG")
        assert logger1 is logger2

    def test_setup_logger_root_logger(self):
        """Test setting up root logger."""
        logger = setup_logger(level="INFO")
        assert logger.name == "root"

    def test_setup_logger_creates_parent_dirs(self, tmp_path: Path):
        """Test that setup_logger creates parent directories for log file."""
        log_file = tmp_path / "subdir" / "nested" / "test.log"
        logger = setup_logger("test_mkdir", level="INFO", log_file=log_file, console=False)
        handler = logger.handlers[0]
        assert isinstance(handler, RotatingFileHandler)
        assert handler.baseFilename  # type: ignore[attr-defined]

    def test_setup_logger_force_clears_handlers(self):
        """Test that force=True clears existing handlers."""
        logger = setup_logger("test_force", level="INFO")
        assert len(logger.handlers) > 0
        setup_logger("test_force", level="DEBUG", force=True)
        assert len(logger.handlers) == 1


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger."""
        logger = get_logger("test_get")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_get"

    def test_get_logger_root(self):
        """Test getting root logger."""
        logger = get_logger()
        assert logger.name == "root"


class TestConvenienceFunctions:
    """Tests for convenience logging functions."""

    def test_debug_function(self, caplog: pytest.LogCaptureFixture):
        """Test debug convenience function."""
        with caplog.at_level(logging.DEBUG):
            debug("test debug message")
            assert any("test debug message" in record.message for record in caplog.records)

    def test_info_function(self, caplog: pytest.LogCaptureFixture):
        """Test info convenience function."""
        with caplog.at_level(logging.INFO):
            info("test info message")
            assert any("test info message" in record.message for record in caplog.records)

    def test_warning_function(self, caplog: pytest.LogCaptureFixture):
        """Test warning convenience function."""
        with caplog.at_level(logging.WARNING):
            warning("test warning message")
            assert any("test warning message" in record.message for record in caplog.records)

    def test_error_function(self, caplog: pytest.LogCaptureFixture):
        """Test error convenience function."""
        with caplog.at_level(logging.ERROR):
            error("test error message")
            assert any("test error message" in record.message for record in caplog.records)

    def test_critical_function(self, caplog: pytest.LogCaptureFixture):
        """Test critical convenience function."""
        with caplog.at_level(logging.CRITICAL):
            critical("test critical message")
            assert any("test critical message" in record.message for record in caplog.records)

    def test_convenience_function_with_args(self, caplog: pytest.LogCaptureFixture):
        """Test convenience function with format args."""
        with caplog.at_level(logging.INFO):
            info("test %s with %d args", "message", 2)
            assert any("test message with 2 args" in record.message for record in caplog.records)


class TestConfigureRootLogger:
    """Tests for configure_root_logger function."""

    def test_configure_root_logger_basic(self):
        """Test basic root logger configuration."""
        logger = configure_root_logger(level="INFO", force=True)
        assert logger.name == "root"

    def test_configure_root_logger_with_file(self, tmp_path: Path):
        """Test root logger with file handler."""
        log_file = tmp_path / "root.log"
        logger = configure_root_logger(
            level="DEBUG", log_file=str(log_file), console=False, force=True
        )
        file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
        assert len(file_handlers) == 1


class TestGetRootLoggerFallback:
    """Tests for _get_root_logger fallback path."""

    def test_get_root_logger_creates_handler_when_none(self, monkeypatch: pytest.MonkeyPatch):
        """Test that _get_root_logger creates handler when root_logger is None."""
        import logpipe.convenience as conv

        monkeypatch.setattr(conv, "_root_logger", None)
        logger = conv._get_root_logger()
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_get_root_logger_fallback_path(self, monkeypatch: pytest.MonkeyPatch):
        """Test _get_root_logger fallback path creates basic handler."""
        import logpipe.convenience as conv

        monkeypatch.setattr(conv, "_root_logger", None)
        root = logging.getLogger()
        original_handlers = list(root.handlers)
        root.handlers.clear()

        try:
            logger = conv._get_root_logger()
            assert logger is not None
            assert len(logger.handlers) == 1
            assert isinstance(logger.handlers[0], logging.StreamHandler)
        finally:
            root.handlers.clear()
            for h in original_handlers:
                root.addHandler(h)


class TestLogLevelType:
    """Tests for LogLevel type."""

    def test_log_level_values(self):
        """Test LogLevel type accepts valid values."""
        valid_levels: list[LogLevel] = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in valid_levels:
            assert level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
