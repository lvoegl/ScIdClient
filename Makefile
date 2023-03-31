SHELL := /usr/bin/env bash
PACKAGE := scidclient
PYTHON_VERSION := 3.11.1

# Install
.PHONY: install
install:
	poetry install -n
	- poetry run mypy --install-types --non-interactive ./
	poetry run pre-commit install

.PHONY: setup-pyenv
setup-pyenv:
	./scripts/setup_pyenv.sh $(PYTHON_VERSION)

.PHONY: install-pyenv
install-pyenv: setup-pyenv install

# Run
.PHONY: run
run:
	poetry run python $(PACKAGE)/__main__.py

# Build
.PHONY: Build
build:
	poetry build

# Dependencies
.PHONY: gen-requirements
gen-requirements:
	poetry lock -n && poetry export --without-hashes > requirements.txt

# Tests
.PHONY: test
test:
	- poetry run pytest -c pyproject.toml --cov-report=html --cov=scidclient tests/
	poetry run coverage-badge -o assets/images/coverage.svg -f

# Formatting
.PHONY: format
format:
	poetry run pyupgrade --exit-zero-even-if-changed --py311-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
	poetry run black --config pyproject.toml ./
	poetry run docformatter --in-place -r scidclient tests

# Documentation
.PHONY: docs
docs:
	poetry run sphinx-build -M html sphinx docs

# Linting
.PHONY: check-style
check-style:
	- poetry run isort --diff --check-only --settings-path pyproject.toml .
	- poetry run black --diff --check --config pyproject.toml .

.PHONY: mypy
mypy:
	- poetry run mypy --namespace-packages --explicit-package-bases --config-file pyproject.toml .  

.PHONY: lint
lint: check-style mypy

# Vulerabilities
.PHONY: security
security:
	- poetry run safety check --full-report
	poetry run bandit -ll --recursive scidclient tests

# Cleaning
.PHONY: clean
clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf requirements.txt
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf docs
