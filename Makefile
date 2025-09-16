# Revo Python Library Makefile
# Provides common development and build tasks

.PHONY: help install install-dev test test-verbose test-coverage lint format clean build publish docs

# Default target
help: ## Show this help message
	@echo "Revo Python Library - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install the package in production mode
	uv sync

install-dev: ## Install the package with development dependencies
	uv sync --dev

# Testing
test: ## Run all tests
	uv run pytest tests/ -v

test-verbose: ## Run tests with verbose output and short tracebacks
	uv run pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage report
	uv run pytest tests/ --cov=revo --cov-report=html --cov-report=term

test-auth: ## Run only authentication tests
	uv run pytest tests/test_auth.py -v

test-config: ## Run only configuration tests
	uv run pytest tests/test_config.py -v

test-llm: ## Run only LLM tests
	uv run pytest tests/test_llm.py -v

test-tokens: ## Run only token management tests
	uv run pytest tests/test_tokens.py -v

test-fast: ## Run tests excluding slow tests
	uv run pytest tests/ -v -m "not slow"

test-unit: ## Run only unit tests
	uv run pytest tests/ -v -m unit

test-integration: ## Run only integration tests
	uv run pytest tests/ -v -m integration

# Code Quality
lint: ## Run linting checks
	uv run flake8 revo/ tests/
	uv run mypy revo/

format: ## Format code with black and isort
	uv run black revo/ tests/
	uv run isort revo/ tests/

format-check: ## Check if code is properly formatted
	uv run black --check revo/ tests/
	uv run isort --check-only revo/ tests/

# Building and Publishing
build: ## Build the package
	uv build

build-wheel: ## Build wheel distribution
	uv build --wheel

build-sdist: ## Build source distribution
	uv build --sdist

publish-test: ## Publish to test PyPI
	uv publish --repository testpypi

publish: ## Publish to PyPI
	uv publish

# Documentation
docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

docs-serve: ## Serve documentation locally
	@echo "Documentation serving not yet implemented"

# Development
dev-setup: install-dev ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make test' to verify everything is working"

check: format-check lint test ## Run all quality checks

# Cleaning
clean: ## Clean build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean ## Clean everything including virtual environment
	rm -rf .venv/

# Environment
env-create: ## Create virtual environment
	uv venv

env-activate: ## Show command to activate virtual environment
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"

# Examples
examples: ## Run example scripts
	uv run python examples/basic_usage.py
	uv run python examples/config_example.py
	uv run python examples/custom_prefixes.py
	uv run python examples/multiple_models.py

# Dependencies
deps-update: ## Update dependencies
	uv lock --upgrade

deps-show: ## Show dependency tree
	uv tree

deps-outdated: ## Show outdated dependencies
	uv tree --outdated

# Configuration
config-check: ## Check configuration files
	@echo "Checking configuration files..."
	@test -f pyproject.toml && echo "✓ pyproject.toml exists" || echo "✗ pyproject.toml missing"
	@test -f pytest.ini && echo "✓ pytest.ini exists" || echo "✗ pytest.ini missing"
	@test -f env.example && echo "✓ env.example exists" || echo "✗ env.example missing"

# CI/CD helpers
ci-test: ## Run tests for CI environment
	uv run pytest tests/ --tb=short --maxfail=1

ci-lint: ## Run linting for CI environment
	uv run flake8 revo/ tests/
	uv run mypy revo/ --no-error-summary

# Quick development workflow
quick-test: ## Quick test run for development
	uv run pytest tests/ -x -v --tb=short

watch-test: ## Watch for file changes and run tests (requires entr)
	@echo "Watching for changes in Python files..."
	find revo/ tests/ -name "*.py" | entr -c make quick-test

# Release helpers
version: ## Show current version
	@uv run python -c "import revo; print(revo.__version__)"

version-bump: ## Bump version (usage: make version-bump TYPE=patch|minor|major)
	@if [ -z "$(TYPE)" ]; then echo "Usage: make version-bump TYPE=patch|minor|major"; exit 1; fi
	@echo "Bumping $(TYPE) version..."
	@uv run python -c "import tomllib; import tomli_w; data = tomllib.load(open('pyproject.toml', 'rb')); data['project']['version'] = '$(shell uv run python -c "import revo; print(revo.__version__)")'; tomli_w.dump(data, open('pyproject.toml', 'wb'))"

# Database and data (if needed in future)
db-migrate: ## Run database migrations (placeholder)
	@echo "Database migrations not implemented yet"

db-reset: ## Reset database (placeholder)
	@echo "Database reset not implemented yet"

# Monitoring and debugging
debug: ## Run with debug logging
	REVO_LOG_LEVEL=DEBUG uv run python -c "import revo; print('Debug mode enabled')"

profile: ## Profile the application (placeholder)
	@echo "Profiling not implemented yet"

# Security
security-check: ## Run security checks
	@echo "Security checks not implemented yet"

# Backup and restore
backup: ## Backup important files
	@echo "Creating backup..."
	tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz revo/ tests/ examples/ pyproject.toml pytest.ini Makefile README.md

# Help for specific targets
help-test: ## Show help for test-related commands
	@echo "Test Commands:"
	@echo "  test          - Run all tests"
	@echo "  test-verbose  - Run tests with verbose output"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  test-auth     - Run only authentication tests"
	@echo "  test-config   - Run only configuration tests"
	@echo "  test-llm      - Run only LLM tests"
	@echo "  test-tokens   - Run only token management tests"
	@echo "  test-fast     - Run tests excluding slow tests"
	@echo "  test-unit     - Run only unit tests"
	@echo "  test-integration - Run only integration tests"

help-dev: ## Show help for development commands
	@echo "Development Commands:"
	@echo "  dev-setup     - Set up development environment"
	@echo "  install-dev   - Install with development dependencies"
	@echo "  format        - Format code with black and isort"
	@echo "  lint          - Run linting checks"
	@echo "  check         - Run all quality checks"
	@echo "  quick-test    - Quick test run for development"
	@echo "  watch-test    - Watch for changes and run tests"

# Default target when no arguments are provided
.DEFAULT_GOAL := help
