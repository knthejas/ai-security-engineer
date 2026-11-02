# AI Security Engineer

Initial backend foundation for a focused security-operations MVP. The eventual MVP flow is AWS CloudTrail ingestion through incidents and AI investigation; none of those product capabilities are implemented yet.

## Prerequisites

- Python 3.12 or newer
- Docker Desktop with Docker Compose v2 (for local PostgreSQL)

## Run locally

1. Create a local environment file from the safe template:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Create and activate a virtual environment, then install the project and development tools:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -e ".[dev]"
   ```

3. Start PostgreSQL:

   ```powershell
   docker compose up -d db
   ```

4. Apply database migrations:

   ```powershell
   alembic upgrade head
   ```

5. Start the API with reload enabled:

   ```powershell
   uvicorn ai_security_engineer.main:app --reload
   ```

6. Verify the service at [http://localhost:8000/health](http://localhost:8000/health). Interactive API docs are at [http://localhost:8000/docs](http://localhost:8000/docs).

To run the API and database together in containers instead, use:

```powershell
docker compose up --build
```

## Quality checks

With the virtual environment active:

```powershell
ruff check .
ruff format --check .
pytest
```

## Configuration and security

`.env.example` contains local-only development defaults, never real credentials. Do not commit `.env` or any credentials. Future AWS development must use only a dedicated test/lab account with least-privilege access; never connect this project to customer infrastructure.

See [the initial architecture](docs/architecture.md) and [development rules](AGENTS.md).
