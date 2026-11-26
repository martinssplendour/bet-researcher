# ADR 005: Background Jobs

## Status

Accepted (26 Nov 2026). Implementation is deferred until lineup polling is built.

## Context

Two kinds of background work exist:

- **Ticket analysis:** when a user submits a ticket, every match on it is analysed in parallel while the browser shows progress.
- **Scheduled work:** nightly data imports, news and injury updates, odds snapshots, lineup checks before kickoff, recalculating affected matches, and settling finished predictions.

## Decision

1. **Ticket analysis (v1)** runs inside the API process as asyncio tasks. Progress is stored in a jobs table and streamed to the browser with Server-Sent Events. No queue is needed.
2. **Scheduled work** runs in a separate worker process backed by Redis, added when the first scheduled job (lineup polling) is built. At that point choose between:
   - **Celery + Celery Beat:** mature, with built-in periodic scheduling.
   - **arq:** lighter and asyncio-native, which fits FastAPI.

   Redis is added to `docker-compose.yml` at the same time.

## Consequences

- Better: no unused infrastructure early; fewer moving parts while the analysis workflow is built.
- Worse: one decision stays open until the worker is needed.
- Know: job status lives in the database from the start, so moving ticket analysis onto the worker later is straightforward. Celery does not officially support Windows; on Windows the worker runs in Docker or WSL2.

## Alternatives Considered

- Celery + Redis from day one: proven, but adds two services before any scheduled job exists.
- APScheduler inside the API process: simple, but jobs stop when the API restarts and break with more than one API instance.
