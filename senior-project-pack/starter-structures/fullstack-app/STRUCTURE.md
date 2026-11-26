# Fullstack App Starter Structure

Use this when frontend and backend live in one repository.

```text
project_root/
|-- README.md
|-- .env.example
|-- docs/
|-- apps/
|   |-- web/
|   `-- api/
|-- packages/
|   |-- shared/
|   |-- config/
|   `-- ui/
|-- tests/
|   |-- unit/
|   |-- integration/
|   `-- e2e/
|-- deployment/
|-- scripts/
`-- .github/workflows/
```

## Boundary Rules

- `apps/web` owns product UI.
- `apps/api` owns backend boundaries and workflows.
- `packages/shared` owns shared types/contracts only.
- `packages/ui` owns reusable UI primitives.
- Avoid putting business logic into shared packages unless both sides truly need it.
- Use one service per file inside each app or package.
- Avoid generic dumping-ground files like `services.ts`, `helpers.ts`, or `utils.ts` when the logic belongs to a specific feature.

## Minimum Senior Checks

- API contract is documented.
- Frontend and backend config are separated.
- E2E tests cover critical user journeys.
- CI can test changed apps independently if the repo grows.
