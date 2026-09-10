# EssenceMatch

EssenceMatch is a local wellness recommendation app that matches a user's
free-text wellness goal or symptom description to a small seeded catalog of
essence items. Recommendations are informational wellness guidance only; they
are not medical advice, diagnosis, or treatment.

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/luisfponce/essence_match/actions/workflows/ci.yml/badge.svg)](https://github.com/luisfponce/essence_match/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-20-green.svg)](https://nodejs.org/)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Docker (recommended)](#docker-recommended)
  - [Local development](#local-development)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

- Browse the seeded essence catalog.
- Submit a free-text wellness prompt and receive deterministic matches.
- JWT-based user registration and login.
- Health endpoint for service monitoring.
- Docker Compose stack with backend, frontend, PostgreSQL, and Redis.
- Alembic scaffolding for future database migrations.

## Tech Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| Frontend    | React, TypeScript, Vite     |
| Backend     | FastAPI, SQLAlchemy         |
| Database    | PostgreSQL 17               |
| Cache/State | Redis                       |
| Proxy       | Caddy (optional)            |
| CI          | GitHub Actions              |

## Prerequisites

- Docker Engine 20.10+ and Compose v2 plugin
- Node.js 20+
- Python 3.12+
- GNU Make (optional)

## Installation

```bash
git clone https://github.com/luisfponce/essence_match.git
cd essence_match
cp .env.example .env
```

## Configuration

| Variable         | Purpose                              | Default                                           |
|------------------|--------------------------------------|---------------------------------------------------|
| `DATABASE_URL`   | PostgreSQL connection string         | `postgresql+psycopg://app:change-me@postgres:5432/app` |
| `REDIS_URL`      | Redis connection string              | `redis://redis:6379/0`                            |
| `JWT_SECRET_KEY` | Secret for auth token signing        | `change-this-local-development-secret`            |

See `.env.example` for the full set of variables.

## Usage

### Docker (recommended)

```bash
make up
```

Open `http://127.0.0.1:8080`. API traffic is proxied through the frontend
container under `/api/v1`; browsers should not call internal Compose hostnames
such as `backend` directly.

```bash
make down
```

### Local development

Copy the configuration contract first so local processes and Compose share
the same values:

```bash
cp .env.example .env
```

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

The local backend needs a reachable `DATABASE_URL`. The Compose PostgreSQL service
can provide that database when running locally.

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API Reference

| Method | Endpoint                  | Purpose                  |
|--------|---------------------------|--------------------------|
| GET    | `/api/v1/health`          | Service health check     |
| GET    | `/api/v1/items`           | List catalog items       |
| POST   | `/api/v1/recommendations` | Get wellness suggestions |
| POST   | `/api/v1/auth/register`   | Register user            |
| POST   | `/api/v1/auth/login`      | Obtain JWT token         |

## Development

```bash
make lint
make test
make build
```

`make lint` currently runs the frontend lint task. Backend linting is
configured through Ruff and available after installing backend development
dependencies.

## Testing

```bash
cd backend && pytest
cd frontend && npm run lint
cd frontend && npm run test -- --run
cd frontend && npm run build
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.

## Disclaimer

Recommendations are informational wellness guidance only. They are not medical
advice, diagnosis, or treatment.