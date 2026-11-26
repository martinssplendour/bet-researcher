# Frontend App Starter Structure

Use this for web apps, dashboards, admin tools, and client-side products.

```text
project_root/
|-- README.md
|-- .env.example
|-- docs/
|   |-- architecture/
|   |-- development/
|   |-- operations/
|   `-- decisions/
|-- src/
|   |-- app/
|   |-- pages/
|   |-- features/
|   |-- components/
|   |-- hooks/
|   |-- services/
|   |-- state/
|   |-- styles/
|   `-- utils/
|-- tests/
|   |-- unit/
|   |-- integration/
|   `-- e2e/
|-- public/
|-- scripts/
`-- .github/workflows/
```

## Boundary Rules

- `pages/` owns route-level composition.
- `features/` owns domain-specific UI and workflows.
- `components/` owns reusable presentational pieces.
- `services/` owns API clients and browser integrations.
- `state/` owns shared client state.
- `utils/` stays generic.
- Use one service/client per file.
- Keep feature logic inside the relevant feature folder instead of large global helper files.

## Minimum Senior Checks

- Loading, empty, error, and success states exist.
- Forms validate before submission.
- API errors are visible and recoverable.
- Critical workflows have E2E tests.
- Accessibility basics are checked.
