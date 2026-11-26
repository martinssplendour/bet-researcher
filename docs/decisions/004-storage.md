# ADR 004: Storage

## Status

Accepted (26 Nov 2026)

## Context

The engine stores fetched match data (to save API requests), analysis jobs and their progress, and every analysis for the track record.

## Decision

SQLAlchemy 2 with Alembic migrations. SQLite for local development, Postgres in production. The database is chosen by `DATABASE_URL`.

## Consequences

- Better: no setup needed locally. Moving to Postgres is a configuration change.
- Worse: SQLite has limited concurrent writes; fine for one developer, not for production traffic.
- Know: all database access goes through `repositories/`. Queries use the ORM or bound parameters, never string building.

## Alternatives Considered

- Postgres from day one (Docker): more realistic, but extra setup before any feature exists.
- JSON files: no migrations, no queries; outgrown quickly.
