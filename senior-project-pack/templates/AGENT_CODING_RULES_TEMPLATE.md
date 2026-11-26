# Agent Coding Rules

Use this file as instructions for AI coding agents and human contributors. The goal is to keep the codebase modular, readable, testable, and easy to change.

## Core Rule

Do not put too much logic in one file.

Every meaningful module should have one clear responsibility. Prefer many small, well-named files over one large file containing unrelated functions, services, utilities, and workflow logic.

## Service File Rule

Use one service per file.

Good:

```text
app/services/
|-- user_service.py
|-- billing_service.py
|-- notification_service.py
|-- report_generation_service.py
```

Avoid:

```text
app/services/
`-- services.py
```

Avoid files like:

- `services.py`
- `helpers.py`
- `utils.py`
- `manager.py`
- `business_logic.py`
- `everything.py`

These names are only acceptable for very small generic modules. If the file grows or mixes responsibilities, split it.

## Function Grouping Rule

A file should contain functions that belong to the same concept.

Good:

```text
app/utils/
|-- date_formatting.py
|-- slug_generation.py
`-- password_validation.py
```

Avoid:

```text
app/utils/
`-- helpers.py
```

Do not create one file with many unrelated functions just because they are all "helpers."

## Recommended File Pattern

For each feature or domain, use focused files:

```text
app/
|-- api/
|   `-- user_routes.py
|-- services/
|   `-- user_service.py
|-- repositories/
|   `-- user_repository.py
|-- domain/
|   `-- user.py
|-- schemas/
|   `-- user_schemas.py
```

Each file should answer one question:

- Route file: how does the outside world call this feature?
- Service file: what workflow or use case happens?
- Repository file: how is data loaded or saved?
- Domain file: what are the rules and entities?
- Schema file: what does input/output look like?

## Agent Instructions

When generating or editing code:

- Create separate files for separate services.
- Keep route/controller files thin.
- Put business logic in service or domain files.
- Put persistence logic in repository files.
- Put external API calls in integration/client files.
- Avoid large mixed-purpose files.
- Split a file when it starts owning more than one responsibility.
- Name files after the responsibility they own.
- Do not hide business logic in `utils`, `helpers`, or generic scripts.
- Add tests near the same responsibility level as the code being tested.

## Split File Triggers

Split a file when:

- It contains more than one service.
- It mixes API, business logic, and database access.
- It has unrelated utility functions.
- It becomes hard to name with one specific noun.
- Tests for the file need many unrelated fixtures.
- A change to one feature risks breaking another unrelated feature.

## Acceptable Exceptions

Small projects can start with fewer files, but the same boundary rules apply.

Acceptable:

- A tiny script with one purpose.
- A small utility file with closely related functions.
- Framework-required entry files like `main.py`, `app.tsx`, or `index.ts`.

Not acceptable:

- One file containing all routes.
- One file containing all services.
- One file containing database, API, validation, and business logic.
- One generic helper file that becomes a dumping ground.

## Review Checklist

- [ ] Each service has its own file.
- [ ] Each file has one clear responsibility.
- [ ] Route/controller files are thin.
- [ ] Business logic is not hidden in helpers.
- [ ] Repository files only handle persistence.
- [ ] Integration files only handle external systems.
- [ ] No file is a dumping ground for unrelated functions.
- [ ] New files are named after the concept they own.

