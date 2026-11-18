SHELL := /bin/bash
COMPOSE_DEV := docker compose \
    -f ./deployments/compose.development.yml \
    --env-file .env.dev \
    -p docssistant-dev

.PHONY: create_migration dev install install_js_deps install_py_deps install_py_dev_deps format format_js format_py migrations_downgrade_dev migrations_upgrade_dev test test_unit test_py_unit

all: install

###
# installation
###

install:
	${MAKE} install_js_deps
	${MAKE} install_py_dev_deps
	${MAKE} install_py_deps

install_js_deps:
	@echo ">>> installing javascript dependencies"
	pnpm install

install_py_dev_deps:
	@echo ">>> installing python development dependencies"
	python3 -m venv .venv
	source .venv/bin/activate && \
		pip install -r pip-requirements.txt && \
		pip install -r dev-requirements.txt && \
		deactivate

install_py_deps:
	@echo ">>> installing python dependencies"
	python3 -m venv .venv
	source .venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate

###
# docker
###

dev:
	$(COMPOSE_DEV) \
		up \
		--build

###
# database
###

migrations_downgrade_dev:
	$(COMPOSE_DEV) \
		run \
		--build \
		--rm alembic \
		downgrade -1

migrations_upgrade_dev:
	$(COMPOSE_DEV) \
		run \
		--build \
		--rm alembic \
		upgrade head

create_migration:
	test -n "$(MESSAGE)" || (echo 'Usage: make create_migration MESSAGE="adds boats table"' && exit 1)
	$(COMPOSE_DEV) \
		 run \
		--build \
		 --rm alembic \
		revision --autogenerate -m "$(MESSAGE)"

###
# formatting
###

format:
	${MAKE} format_js
	${MAKE} format_py

format_js:
	@echo ">>> formatting javascript files"
	pnpm format

format_py:
	@echo ">>> formatting python files"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m isort . && \
		python3 -m black .

###
# linting
###

lint:
	${MAKE} lint_py

lint_py:
	@echo ">>> linting python files"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m flake8 .

###
# testing
###

test:
	${MAKE} test_integration
	${MAKE} test_unit

test_integration:
	${MAKE} test_py_integration

test_py_integration:
	@echo ">>> running python integration tests"
	python3 -m venv .venv
	source .venv/bin/activate && \
		./scripts/test_py_integration.bash

test_unit:
	${MAKE} test_py_unit

test_py_unit:
	@echo ">>> running python unit tests"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m pytest test/unit
