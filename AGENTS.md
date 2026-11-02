# Development rules

## Scope and architecture

- Keep the MVP focused on AWS CloudTrail ingestion, normalization, detection rules, incidents, AI investigation, and dashboard work as it is explicitly requested.
- Prefer a simple modular monolith over microservices.
- Do not add AWS ingestion, detection logic, AI agents, response automation, persistence models, or frontend features unless the task explicitly requests them.
- Place HTTP transport in `api/`, shared concerns in `core/`, persistence code in `db/`, data contracts in `schemas/`, and domain orchestration in `services/`.

## Security

- Never commit or log secrets, API keys, AWS credentials, tokens, passwords, private keys, or customer data.
- Use only a dedicated AWS test/lab account during development; never connect to customer infrastructure.
- Apply least privilege to AWS access and document permissions before introducing integrations.
- Design new persistence and authorization features for tenant isolation.
- Make security-sensitive actions auditable.
- AI must not directly execute destructive security actions in the MVP.

## Quality

- Target Python 3.12+ and use type hints for new Python code.
- Add or update pytest coverage for behavior changes.
- Run `ruff check .`, `ruff format --check .`, and `pytest` before completing a change when tooling is available.
- Keep configuration in environment variables; update `.env.example` with safe placeholder or local-only values only.
