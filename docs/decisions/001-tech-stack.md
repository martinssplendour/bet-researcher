# ADR 001: Tech Stack

## Status

Accepted (26 Nov 2026)

## Context

The app needs statistics (ratings, Poisson scorelines, later back-testing and calibration), calls to an AI provider and a football data API, and a polished web interface with live progress.

## Decision

- **Engine:** Python 3.12, uv, FastAPI, Pydantic v2, httpx, SQLAlchemy 2 + Alembic, pytest, ruff, mypy.
- **Web:** Next.js (App Router) + TypeScript, Tailwind CSS, TanStack Query, Vitest, Playwright.
- **Layout:** one repository, `apps/engine` and `apps/web`.

## Consequences

- Better: Python has the strongest statistics and AI tooling. The domain maths stays simple and testable.
- Worse: two toolchains to maintain; types are shared through the API contract, not code.
- Know: Python 3.12 rather than 3.13, because 3.12 is installed and fully supported. Upgrade later if needed.

## Alternatives Considered

- TypeScript only: workable for v1 maths, but back-testing and calibration are much harder.
- Python only (e.g. Streamlit): fine for prototypes, weak for a polished product UI.
