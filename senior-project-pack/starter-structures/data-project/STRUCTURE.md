# Data Project Starter Structure

Use this for pipelines, analytics, ML datasets, reporting, and batch processing.

```text
project_root/
|-- README.md
|-- .env.example
|-- docs/
|   |-- architecture/
|   |-- data/
|   |-- operations/
|   `-- decisions/
|-- src/
|   |-- ingestion/
|   |-- transforms/
|   |-- validation/
|   |-- storage/
|   |-- reporting/
|   `-- core/
|-- tests/
|   |-- unit/
|   |-- integration/
|   `-- data-quality/
|-- scripts/
|-- notebooks/
|-- config/
`-- .github/workflows/
```

## Source Control Rules

Commit:

- Code
- Schemas
- Small fixtures
- Data contracts
- Pipeline definitions

Do not commit:

- Production data
- Large generated datasets
- Secrets
- Model checkpoints
- Personal exports

## Minimum Senior Checks

- Data source and owner are documented.
- Data quality checks exist.
- Regeneration process is documented.
- Retention and privacy rules are documented.
- Pipeline failures are observable.
- Ingestion, transformation, validation, storage, and reporting code are separated by file and module.
- Avoid one pipeline file containing every step unless it is a tiny single-purpose script.
