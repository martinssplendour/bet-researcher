# Architecture Overview

## What the system does

A user submits a ticket (text or bet slip image). The engine reads the picks, analyses every match in parallel, and returns per-match research plus a combined ticket verdict. The method is in [../method.md](../method.md).

## System context

```text
                +------------------+
  Browser  ---> |  Web (Next.js)   |   ticket input, progress, results pages
                +--------+---------+
                         | HTTP + Server-Sent Events (progress)
                +--------v---------+
                |  Engine (Python) |   analysis workflow, maths, storage
                +--+------------+--+
                   |            |
      +------------v--+      +--v------------------+
      | API-Football  |      | Google Gemini       |
      | match data    |      | news search, analyst|
      +---------------+      | slip image reading  |
                             +---------------------+
                   Database: PostgreSQL (Docker locally, managed in production)
```

## Request lifecycle (one ticket)

1. Web sends the ticket text or image to the engine.
2. Engine reads the picks (Gemini for images), validates them, and creates one job per match.
3. Each match job runs on its own: fetch data → history window → ratings → baseline → news scout → analyst → predictions. Progress streams back to the browser.
4. When all jobs finish, the engine combines them into the ticket verdict.
5. Every analysis is saved with its inputs, for the track record.

## Module boundaries (engine)

| Module | Owns | Must not |
| --- | --- | --- |
| `core/` | settings (fail fast), logging, error types | contain business rules |
| `domain/` | the method's maths and rules: history window, league averages, ratings, expected goals, scorelines, markets, odds, verdicts, tickets | do I/O, call APIs, read settings |
| `integrations/` | API-Football client, Gemini client: HTTP, retries, response validation | contain business rules |
| `repositories/` | storing and loading fixtures, players, analyses | call external APIs |
| `services/` | workflows such as match analysis and ticket analysis | contain HTTP or SQL details |
| `prompts/` | versioned Gemini prompts | contain code |
| `api/` | thin HTTP routes | contain business logic |

`domain/` is pure, which makes it fast to test and safe to change: the same inputs always give the same numbers.

## Where failures happen

| Failure | Handling |
| --- | --- |
| API-Football down or over quota | Retry with backoff; use cached data; mark the match "data unavailable" |
| Gemini error or bad output | Validate against the schema; on failure use the baseline with a "no AI adjustment" flag |
| Gemini text with invented numbers | Rejected by the fact-sheet number check |
| Bet slip image unreadable | Ask the user to confirm or edit the picks |

## Trade-offs accepted

- **Two languages** (Python engine, TypeScript web): better maths and AI tooling, at the cost of two toolchains.
- **No job queue in v1:** ticket analysis runs as asyncio tasks with a jobs table. Scheduled work (lineup polling, imports, settling) gets a worker and Redis when it is built ([ADR 005](../decisions/005-background-jobs.md)).
- **Modular monolith:** one web app, one Python app, one worker, one database, until real usage proves otherwise.
- **Poisson independence:** slightly under-predicts low draws; Dixon-Coles correction later.
