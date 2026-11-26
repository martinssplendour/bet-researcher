# Backend API Starter Structure

Use this for REST, GraphQL, RPC, or service APIs.

```text
project_root/
|-- README.md
|-- .env.example
|-- docs/
|   |-- architecture/
|   |-- api/
|   |-- development/
|   |-- operations/
|   `-- decisions/
|-- app/
|   |-- api/
|   |-- services/
|   |-- domain/
|   |-- repositories/
|   |-- integrations/
|   |-- core/
|   `-- main.py
|-- tests/
|   |-- unit/
|   |-- integration/
|   `-- e2e/
|-- scripts/
|-- config/
|-- deployment/
`-- .github/workflows/
```

## Boundary Rules

- Routes parse requests and format responses.
- Services coordinate workflows.
- Each service gets its own file.
- Domain owns rules.
- Repositories own persistence.
- Integrations own external services.
- Core owns config, logging, errors, and app wiring.
- Do not create a single `services.py` or `helpers.py` file containing unrelated logic.

## Minimum Files

- `README.md`
- `.env.example`
- `docs/architecture/overview.md`
- `docs/api/openapi.yaml`
- `docs/decisions/001-initial-architecture.md`
- `.github/pull_request_template.md`
