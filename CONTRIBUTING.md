# Contributing to EssenceMatch

Thank you for your interest in improving EssenceMatch. This guide explains how
to set up a development environment, propose changes, and submit a pull
request.

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).
Reports of unacceptable behavior can be sent to the contacts listed in
[SECURITY.md](SECURITY.md).

## Development Setup

### Prerequisites

- Docker Engine 20.10+ with the Compose v2 plugin
- Python 3.12+
- Node.js 20+
- GNU Make (optional, for the convenience targets)

### Fork and Clone

```bash
git clone https://github.com/<your-username>/<repo>.git
cd <repo>
cp .env.example .env
```

### Run the Stack

```bash
make up
```

The application is served on `http://127.0.0.1:8080`. Tear it down with
`make down`.

### Local Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

### Local Frontend

```bash
cd frontend
npm install
npm run dev
```

## Reporting Issues

- **Bugs**: use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).
- **Features**: use the
  [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).
- **Security vulnerabilities**: follow [SECURITY.md](SECURITY.md); do **not**
  file a public issue.

Search existing issues before opening a new one. Include reproduction steps,
expected/actual behavior, and environment details.

## Pull Request Workflow

1. Fork the repository and create a topic branch from `main`:
   ```bash
   git checkout -b feat/short-description
   ```
2. Make your changes in logical commits. Follow [Conventional Commits][cc]
   for commit messages:
   - `feat:` for new user-facing functionality
   - `fix:` for bug fixes
   - `docs:` for documentation only
   - `chore:` for tooling, configuration, or non-functional changes
   - `test:` for adding or fixing tests
   - `refactor:`, `perf:`, `ci:` as appropriate
3. Keep changes focused. One logical change per PR is easier to review and
   revert.
4. Update documentation, fixtures, or seed data when behavior changes.
5. Run the full quality suite locally before pushing:
   ```bash
   make lint
   make test
   make build
   ```
6. Push to your fork and open a pull request against `main` using the
   [PR template](.github/PULL_REQUEST_TEMPLATE.md).
7. Respond to review feedback. Squash fix-up commits before merging unless the
   reviewer asks otherwise.

## Coding Standards

- **Backend**: Python 3.12, Ruff for lint/format, type hints on public APIs,
  pytest for tests. Keep modules small and focused; put business logic in
  `services/`, persistence in `repositories/`, and HTTP wiring in `api/`.
- **Frontend**: TypeScript, ESLint, Vitest + React Testing Library, Vite for
  the dev server and production builds. Prefer functional components and hooks.
- **API**: every endpoint should have an integration or unit test, a Pydantic
  schema, and an entry in the `README.md` API reference table.
- **Wellness disclaimer**: any new endpoint or UI surface that surfaces
  recommendations must preserve the informational-only disclaimer.

## Testing

- Backend tests run against an in-memory SQLite fixture; no live MariaDB
  required for the default `pytest` invocation.
- Frontend tests use Vitest; run with `npm run test -- --run` for a single
  CI-style pass.
- Add regression tests for bug fixes and example tests for new features.

## Release Process (maintainers)

1. Update `CHANGELOG.md` under a new version heading.
2. Bump versions in `backend/pyproject.toml` and `frontend/package.json`.
3. Tag the commit with the version (`vX.Y.Z`).
4. Push tags and let CI publish artifacts.

[cc]: https://www.conventionalcommits.org/
