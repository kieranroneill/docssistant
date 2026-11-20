<div align="center">

[![License: CC0-1.0](https://img.shields.io/github/license/kieranroneill/docssistant)](https://github.com/kieranroneill/docssistant/blob/main/LICENSE)

</div>

<h1 align="center">
  Docssistant
</h1>

<p align="center">
    Docssistant is a document chat assistant that uses retrieval-augmented generation (RAG) to answer questions about your documents and cite its sources.
</p>

---

### Table of contents

* [1. Overview](#-1-overview)
  - [1.1. Project structure](#11-project-structure)
- [2. Usage](#-2-usage)
  - [2.1. Requirements](#21-requirements)
  - [2.2. Getting Started](#22-getting-started)
- [3. Development](#-3-development)
  - [3.1. Requirements](#31-requirements)
  - [3.2. Start Docker](#32-start-docker)
* [4. Appendix](#-4-appendix)
  - [4.1. Useful commands](#41-useful-commands)
  - [4.2. Database migrations](#42-database-migrations)
* [5. How to contribute](#-5-how-to-contribute)
* [6. License](#-6-license)

## 🔭 1. Overview

### 1.1. Project structure

```text
.
├─ .documents/                              <-- Raw documents that are indexed by the indexer
│   └── ...
├─ api/                                     <-- API source files - uses a functional layering approach
│   ├── <package_name>/
│   │   └── ...
│   ├── main.py                             <-- Entrypoint file
│   └── ...
├─ build/
│   ├── package/                            <-- Docker image files
│   │   ├── <service-name>/
│   │   │   ├── Dockerfile
│   │   │   └── Dockerfile.development
│   │   └── ...
│   └── ...
├─ deployments/                             <-- Container orchestration configurations
│   ├── compose.yml
│   ├── compose.development.yml
│   ├── compose.test.yml
│   └── ...
├─ indexer/                                 <-- Indexer worker - scans for documents and indexes them
│   ├── main.py                             <-- Entrypoint file
│   └── ...
├─ libs/                                    <-- Library source files - uses a functional layering approach
│   ├── <package_name>/
│   │   └── ...
│   └── ...
├─ migrations/                              <-- Alembic migrations
│   ├── versions/
│   │   ├── 19700101000000_create_a_table.sql
│   │   └── ...
│   └── ...
├─ web/                                     <-- Web UI source files
│   ├── main.ts                             <-- Entrypoint file
│   └── ...
├── commitlint.config.ts                    <-- Commitlint configuration
├── dev-requirements.txt                    <-- Python development dependencies
├── LICENSE                                 <-- Project license
├── Makefile                                <-- Make commands
├── package.json                            <-- JavaScript dependencies for tools and web UI
├── pip-requirements.txt                    <-- Defines the pip version
├── prettier.config.ts                      <-- Prettier configuration for formatting JS/TS files
├── pyproject.toml                          <-- Python project configuration file
├── README.md
├── requirements.txt                        <-- Python dependencies
└── ...
```

<sup>[Back to top ^][table-of-contents]</sup>

## 🪄 2. Usage

#### 2.1. Requirements

- [Docker](https://docs.docker.com/engine/install/)

<sup>[Back to top ^][table-of-contents]</sup>

#### 2.2. Getting Started

1. Add a file the relevant `.env` files to the `configs/` directory for each of the services.

2. Using Docker compose, you can run the orchestration file using:

```bash
$ make start
```

<sup>[Back to top ^][table-of-contents]</sup>


## 🛠️ 3. Development

### 3.1. Requirements

- [Docker](https://docs.docker.com/engine/install/)

<sup>[Back to top ^][table-of-contents]</sup>

#### 3.2. Start Docker

1. Using Docker compose, you can run the orchestration file using:

```bash
$ make dev
```

<sup>[Back to top ^][table-of-contents]</sup>

## 📑 4. Appendix

### 4.1. Useful commands

| Command                                                     | Description                                                          |
|-------------------------------------------------------------|----------------------------------------------------------------------|
| `make create_migration MESSAGE="create conversations table"` | Starts the Docker `api` service and runs autogenerates migrations.   |
| `make dev`                                                  | Runs the platform in development mode via Docker.                    |
| `make migration_downgrade`                                   | Downgrades the database migrations by a version.                     |
| `make migration_downgrade_dev`                               | Downgrades the database migrations by a version (development only).  |
| `make migration_upgrade`                                     | Upgrades the database migrations.                                    |
| `make migration_upgrade_dev`                                 | Upgrades the database migrations (development only).                 |
| `make format`                                               | Formats soruce code files.                                           |
| `make install`                                              | Installs all the dependencies - including development dependencies.  |
| `make install_js_deps`                                      | Installs the JavaScript dependencies.                                |
| `make install_py_deps`                                      | Installs the Python application dependencies.                        |
| `make install_py_dev`                                       | Installs the Python dependencies that inlucde tools for development. |
| `make lint_py`                                              | Lints Python soruce files.                                           |
| `make start`                                                | Runs the platform in production mode via Docker.                     |
| `make test`                                                 | Runs all tests.                                                      |
| `make test_py_unit`                                         | Runs Python tests.                                                   |
| `make test_unit`                                            | Runs all unit tests.                                                 |

<sup>[Back to top ^][table-of-contents]</sup>

### 4.2. Database migrations

Database migrations are managed with [Alembic](https://alembic.sqlalchemy.org/en/latest/) and run through Docker, so they use the same environment as the API service.

Use the following commands to create, apply, or roll back migrations:

```shell
make create_migration MESSAGE="add conversations table"
make migration_upgrade
make migration_downgrade
```

For development, the matching commands are:

```shell
make migration_upgrade_dev
make migration_downgrade_dev
```

- `create_migration` generates a new Alembic revision from SQLAlchemy model changes.
- `migration_upgrade` applies all pending migrations in the production Compose setup.
- `migration_downgrade` rolls back the latest migration in the production Compose setup.
- `migration_upgrade_dev` applies all pending migrations in the development Compose setup.
- `migration_downgrade_dev` rolls back the latest migration in the development Compose setup.

> ⚠️ **NOTE:** The `MESSAGE` argument is required when creating a migration because it becomes the migration description.

<sup>[Back to top ^][table-of-contents]</sup>

## 👏 5. How to contribute

Please read the [**contributing guide**](./CONTRIBUTING.md) to learn about the development process.

<sup>[Back to top ^][table-of-contents]</sup>

## 📄 6. License

Please refer to the [LICENSE](./LICENSE) file.

<sup>[Back to top ^][table-of-contents]</sup>

<!-- links -->

[table-of-contents]: #table-of-contents
