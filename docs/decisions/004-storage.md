# ADR 004: Storage (PostgreSQL)

## Status

Accepted (26 Nov 2026). Replaces the earlier choice of SQLite for local development.

## Context

The engine stores fixtures and results, team and player statistics, injuries, predicted and confirmed lineups, odds snapshots, every prediction with its model version and inputs, final outcomes for back-testing, and analysis jobs. Background workers will write at the same time as the API.

## Decision

PostgreSQL everywhere:

- **Local:** Postgres 17 from `docker-compose.yml`, bound to localhost only.
- **Production:** managed Postgres, chosen in the hosting decision record.
- **Access:** SQLAlchemy 2 (async, psycopg 3) with Alembic migrations. `DATABASE_URL` is required; the engine will not start without it.

## Consequences

- Better: development matches production. Concurrent writes work. JSONB can hold raw API payloads and analysis inputs.
- Worse: Docker is needed for local development.
- Know: all database access goes through `repositories/`. Each concurrent task uses its own session, because async SQLAlchemy sessions must not be shared between tasks. Queries use the ORM or bound parameters, never string building.

## Alternatives Considered

- SQLite for development: no setup, but development drifts from production and concurrent writes fail once workers exist.
- JSON files: no migrations or queries; outgrown quickly.
