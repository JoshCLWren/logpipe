# Repository Guidelines

## Project Structure & Module Organization
The main package code lives in the `logpipe` directory. The package provides:
- `logger.py` - Core logger setup with rotating file and console handlers
- `convenience.py` - Convenience logging functions using a root logger
- `__init__.py` - Public API exports

No entrypoint module exists as logpipe is a library package.

## Build, Test, and Development Commands
- `uv sync --all-extras`: Install dependencies via uv.
- `pytest` or `make pytest`: Run the test suite.
- `make lint`: Run ruff and pyright checks.

## Getting Started
When working on logpipe:
1. Run `uv sync --all-extras` to install all dependencies
2. Run `source .venv/bin/activate` to activate the virtual environment
3. Run `pytest` to verify tests pass
4. Make changes to the logger or convenience functions
5. Run `make lint` before committing

## Git Worktrees (Parallel Work)
Use git worktrees to work on multiple cards in parallel without branch conflicts:
- Create a branch per card: `git switch -c card/short-slug`
- Add a worktree: `git worktree add ../logpipe-<slug> card/short-slug`
- Work only in that worktree for the card; run tests there.
- Keep the branch updated: `git fetch` then `git rebase origin/main` (or merge).
- When merged, remove it: `git worktree remove ../logpipe-<slug>`
- Clean stale refs: `git worktree prune`
- WIP limit: 3 cards total in progress across all worktrees.

## Test Coverage Requirements
- Current target: 96% coverage threshold (configured in `pyproject.toml`)
- Always run `pytest --cov=logpipe --cov-report=term-missing` to check missing coverage
- When touching logger logic or convenience functions, ensure tests are added to maintain coverage
- Strategies for increasing coverage:
  - Add tests for remaining uncovered edge cases in file rotation
  - Add tests for complex error handling paths in logger setup
  - Add tests for different logging level configurations

## Coding Style & Naming Conventions
Follow standard PEP 8 spacing (4 spaces, 100-character soft wrap) and favor descriptive snake_case for functions and variables. Keep public functions annotated with precise types. Use Literal types for string parameters with fixed values (e.g., `LogLevel`).

Ruff configuration (from `pyproject.toml`):
- Line length: 100 characters
- Python version: 3.13
- Enabled rules: E, F, I, N, UP, B, C4, D, ANN401
- Ignored: D203, D213, E501
- Code comments are discouraged - prefer clear code and commit messages

## Pre-commit Hook
A pre-commit hook is installed in `.git/hooks/pre-commit` that automatically runs:
- Check for type/linter ignores in staged files
- Run the shared lint script (`scripts/lint.sh`)

The lint script runs:
- Python compilation check
- Ruff linting
- Any type usage check (ruff ANN401 rule)
- Pyright type checking

The hook will block commits containing `# type: ignore`, `# noqa`, `# ruff: ignore`, or `# pylint: ignore`.

To test the hook manually: `make githook` or `bash scripts/lint.sh`

## Code Quality Standards
- Run linting after each change:
  - `make lint` or `bash scripts/lint.sh`
- Use specific types instead of `Any` in type annotations (ruff ANN401 rule)
  - Exception: Convenience functions use `**kwargs: Any` to match logging module signatures
- Run tests when you touch logic or input handling:
  - `pytest`
- Always write a regression test when fixing a bug.
- If you break something while fixing it, fix both in the same PR.
- Do not use in-line comments to disable linting or type checks.
- Do not narrate your code with comments; prefer clear code and commit messages.

## Style Guidelines
- Keep functions explicit and descriptive (snake_case), and annotate public functions with precise types.
- Use Literal types for string parameters with fixed values (e.g., `LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]`).
- Prefer pathlib.Path for file path operations over strings.
- Follow standard library patterns for logging API compatibility.

## Branch Workflow
- Always create a feature branch from `main` before making changes:
  - `git checkout -b feature-name`
  - Use descriptive names like `fix-bug` or `add-feature`
- Push the feature branch to create a pull request
- After your PR is merged, update your local `main`:
  - `git checkout main`
  - `git pull`
  - Delete the merged branch: `git branch -d feature-name`

## Testing Guidelines
- Automated tests live in `tests/` and run with `python -m pytest` (or `make pytest`).
- When adding tests, keep `pytest` naming like `test_logger_setup`, `test_convenience_functions`.
- Use appropriate fixtures from `conftest.py` for testing dependencies.
- Test both successful operations and error conditions.
- Test file rotation behavior with different size limits.
- Test logger configuration with and without file handlers.

## Commit & Pull Request Guidelines
- Use imperative, component-scoped commit messages (e.g., "Add file rotation support")
- Bundle related changes per commit
- PR summary should describe user impact and testing performed
- For convenience function changes, include usage examples in PR description
