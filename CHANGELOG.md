# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-09

### Added

- FastAPI backend with health, catalog, recommendation, and auth endpoints.
- SQLAlchemy models for `Item` and `User` with MariaDB persistence.
- Deterministic keyword-based recommendation engine.
- Catalog seeded at startup with six essence items.
- JWT-based register and login endpoints.
- React + TypeScript + Vite frontend with catalog browsing and recommendation UI.
- Docker Compose stack for backend, frontend, MariaDB, and Redis.
- GitHub Actions CI running backend pytest and frontend lint, test, and build.
- Alembic scaffolding for future database migrations.
- MIT license, contributing guide, code of conduct, and security policy.

### Notes

- Recommendations are informational wellness guidance only and are **not**
  medical advice, diagnosis, or treatment.