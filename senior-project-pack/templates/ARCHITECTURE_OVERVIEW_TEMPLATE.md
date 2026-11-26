# Architecture Overview

## Purpose

Describe the system's purpose in plain language.

## Users

- Primary users:
- Internal users:
- Admin users:
- External systems:

## Main Workflows

1. [Workflow name]
   - Trigger:
   - Steps:
   - Result:
   - Failure modes:

## System Context

```text
[User/System] -> [Application] -> [Database/External Service]
```

## Core Modules

| Module | Owns | Does Not Own |
| --- | --- | --- |
| `api/` | Request/response boundary | Business rules |
| `services/` | Use cases and workflows | Database implementation details |
| `domain/` | Core rules and entities | HTTP concerns |
| `repositories/` | Persistence | Business decisions |
| `integrations/` | External systems | Core domain rules |
| `core/` | Config, logging, wiring | Feature-specific logic |

## Modularity Rules

- Use one service per file.
- Name each file after the responsibility it owns.
- Keep route/controller files thin.
- Do not place unrelated functions into one large helper file.
- Do not mix API logic, business logic, persistence, and external integrations in the same file.
- Split files when they become hard to describe with one specific responsibility.

Preferred:

```text
app/services/user_service.py
app/services/billing_service.py
app/repositories/user_repository.py
app/integrations/payment_client.py
```

Avoid:

```text
app/services.py
app/helpers.py
app/business_logic.py
```

## Data Flow

Describe how data enters, moves through, and leaves the system.

## Security Boundaries

- Auth boundary:
- Data access boundary:
- Admin boundary:
- External integration boundary:

## Scaling Considerations

- Expected load:
- Current bottlenecks:
- Future bottlenecks:
- Scaling strategy:

## Operational Concerns

- Health checks:
- Logs:
- Metrics:
- Alerts:
- Rollback:

## Known Tradeoffs

| Tradeoff | Reason | Future Revisit Trigger |
| --- | --- | --- |
| [Decision] | [Reason] | [Condition] |
