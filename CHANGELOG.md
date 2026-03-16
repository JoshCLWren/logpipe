# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-03-14

### Added
- Initial release of logpipe
- Logger setup with rotating file and console handlers
- `setup_logger()` function for creating configured loggers
- `get_logger()` function for retrieving existing loggers
- `configure_root_logger()` for setting up the root logger
- Convenience functions: `debug()`, `info()`, `warning()`, `error()`, `critical()`
- Configurable log file rotation with size limits and backup counts
- Custom format support for log messages and timestamps
- Console and file handler support
- Zero external dependencies
- Full type hints with `LogLevel` Literal type
- 96%+ test coverage
- Support for Python 3.13+

### Features
- Rotating file handlers prevent unbounded log file growth
- Named logger support for modular applications
- Convenience functions for quick logging without logger management
- Flexible configuration with sensible defaults
- Type-safe API with full type hints
