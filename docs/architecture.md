# Initial architecture

## Scope

This repository initializes the backend for the first MVP path:

`AWS CloudTrail → ingestion → normalization → detection rules → incidents → AI investigation → dashboard`

Only the HTTP service foundation and local database infrastructure are present today. CloudTrail ingestion, event normalization, rules, incidents, AI investigation, persistence models, and a frontend are explicitly deferred.

## Components

- **FastAPI application**: a modular HTTP service under `src/ai_security_engineer`. It currently exposes only `GET /health` as a liveness endpoint.
- **PostgreSQL**: the intended system-of-record database. Docker Compose supplies a local Postgres 16 instance. SQLAlchemy provides database sessions and Alembic manages schema migrations.
- **Configuration**: `pydantic-settings` reads environment variables and an optional local `.env` file. `.env.example` documents safe local-only values.
- **Quality checks**: pytest covers the health endpoint and Ruff provides linting and formatting.

## Code boundaries

- `api/`: routing and transport concerns.
- `core/`: configuration and future cross-cutting concerns.
- `db/`: database engine, session management, SQLAlchemy models, and migration boundary.
- `schemas/`: future request/response data contracts.
- `services/`: future domain orchestration.

This modular monolith is intentional. New MVP capabilities should be added within these boundaries before considering service extraction.

## Security posture

- Do not store credentials, secrets, customer data, or tokens in version control.
- Development integrations, when added, may use only a dedicated AWS test/lab account with least-privilege credentials.
- Future persistence and access controls must make tenant isolation explicit.
- Security-sensitive actions must be auditable.
- AI may investigate and recommend in the MVP, but must not directly execute destructive security actions.
