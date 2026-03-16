# logpipe

[![CI Status](https://github.com/JoshCLWren/logpipe/workflows/CI/badge.svg)](https://github.com/JoshCLWren/logpipe/actions)

Logger setup with rotating file handlers and convenience functions.

## Features

- **Python 3.13+** with type hints throughout
- **Structured logging** with customizable formatters
- **Rotating file handlers** with configurable size limits and backup counts
- **Console output** support for development
- **Convenience functions** for quick logging (debug, info, warning, error, critical)
- **Zero dependencies** - lightweight and fast
- **Type-safe** API with full type hints

## Installation

```bash
pip install logpipe
```

## Quick Start

### Basic Usage (Convenience Functions)

The simplest way to use logpipe is with the convenience functions:

```python
from logpipe import configure_root_logger, info, debug, error

# Configure the root logger (optional - will use defaults if not called)
configure_root_logger(
    level="INFO",
    log_file="app.log",  # Optional: write to rotating file
    console=True,  # Also output to console
)

# Use convenience functions anywhere
info("Application started")
debug("Debug information", extra_key="value")
error("An error occurred", exc_info=True)
```

### Advanced Usage (Multiple Loggers)

For more control, use `setup_logger` to create named loggers:

```python
from logpipe import setup_logger, get_logger

# Set up a named logger with file rotation
logger = setup_logger(
    name="my_module",
    level="DEBUG",
    log_file="logs/my_module.log",
    max_bytes=10 * 1024 * 1024,  # 10MB per file
    backup_count=5,  # Keep 5 backup files
    console=True,
)

# Use the logger
logger.debug("Detailed debug info")
logger.info("Processing started")
logger.warning("Configuration file not found, using defaults")
logger.error("Failed to process request")
logger.critical("System failure")

# Get the logger elsewhere without reconfiguring
logger = get_logger("my_module")
logger.info("Logger retrieved from cache")
```

### File Rotation

Logpipe automatically rotates log files when they reach the size limit:

```python
from logpipe import configure_root_logger

configure_root_logger(
    log_file="app.log",
    max_bytes=50 * 1024 * 1024,  # 50MB per file
    backup_count=10,  # Keep 10 backup files (app.log.1, app.log.2, etc.)
)

# Log files will be automatically rotated:
# - app.log (current)
# - app.log.1 (most recent backup)
# - app.log.2 (second most recent backup)
# - ... up to backup_count
```

### Custom Formats

Customize log message formatting:

```python
from logpipe import setup_logger

logger = setup_logger(
    name="custom",
    log_format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    date_format="%Y-%m-%d %H:%M:%S",
)
```

## API Reference

### Convenience Functions

- `configure_root_logger(level, log_file, max_bytes, backup_count, log_format, date_format, console, force)` - Configure the root logger used by convenience functions
- `debug(msg, *args, **kwargs)` - Log a debug message
- `info(msg, *args, **kwargs)` - Log an info message
- `warning(msg, *args, **kwargs)` - Log a warning message
- `error(msg, *args, **kwargs)` - Log an error message
- `critical(msg, *args, **kwargs)` - Log a critical message

### Core Functions

- `setup_logger(name, level, log_file, max_bytes, backup_count, log_format, date_format, console, force)` - Set up a logger with rotating file and console handlers
- `get_logger(name)` - Get an existing logger without reconfiguring handlers

### Types

- `LogLevel` - Literal type: `"DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL"`

## Development

### Setup

```bash
# Install dependencies
uv sync --all-extras

# Activate virtual environment
source .venv/bin/activate
```

### Testing

```bash
# Run tests
make pytest

# Run tests with coverage
pytest --cov=logpipe --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Linting

```bash
# Run all linting checks
make lint

# Format code
ruff format .

# Run type checker
pyright .
```

## Project Structure

```
.
├── logpipe/               # Main package
│   ├── __init__.py       # Public API exports
│   ├── logger.py         # Core logger setup functions
│   └── convenience.py    # Convenience logging functions
├── tests/                # Test suite
│   ├── conftest.py       # pytest fixtures
│   └── test_logger.py    # Logger tests
├── scripts/              # Development scripts
│   └── lint.sh          # Linting script
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lockfile
└── README.md            # This file
```

## Code Quality

- **96%+ test coverage** required
- **ruff** for linting and formatting
- **pyright** for static type checking
- **Pre-commit hooks** enforce code quality

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `make pytest`
5. Run linting: `make lint`
6. Commit with conventional commits
7. Push and create a pull request

## License

MIT License - see LICENSE file for details

## Credits

Created by Josh Wren
