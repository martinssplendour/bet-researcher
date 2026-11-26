# ADR 001: Tech Stack

## Status

Accepted (26 Nov 2026). Updated the same day after a stack review.

## Context

The app needs statistics (ratings, Poisson scorelines, later back-testing and calibration), calls to an AI provider and a football data API, scheduled data updates, and a polished web interface with live progress.

## Decision

A **modular monolith**: one web app, one Python app, one worker process (when needed) and one database.

| Area | Choice | Added when |
| --- | --- | --- |
| Web app | Next.js (App Router) + TypeScript | Web phase |
| UI | Tailwind CSS + shadcn/ui | Web phase |
| Charts | Apache ECharts (scoreline heat map, goal distributions, form) | Web phase |
| HTTP API | FastAPI | With the analysis service |
| Engine | Python 3.12, uv, installable package `bet_researcher` (src layout). The `domain/` package is pure and usable without the API. | Now |
| Config and validation | Pydantic v2, pydantic-settings | Now |
| Database | PostgreSQL, SQLAlchemy 2, Alembic ([ADR 004](004-storage.md)) | Data layer |
| Background jobs | See [ADR 005](005-background-jobs.md) | Lineup polling |
| Numerical | NumPy, SciPy (Dixon-Coles fitting), Polars (historical datasets), statsmodels, scikit-learn (calibration, Brier and log loss) | Back-testing and ratings v2 |
| Testing | pytest; Vitest + Playwright | Now; web phase |

Dependencies are added when the feature that needs them is built, not before.

## Consequences

- Better: Python has the strongest statistics and AI tooling. The domain maths is testable without the API, database or website.
- Worse: two toolchains to maintain; types are shared through the API contract, not code.
- Know: every analysis result carries `model_version` and `calculated_at`, so the track record can be judged per model version. Python 3.12 is used because it is installed and fully supported.

## Alternatives Considered

- TypeScript only: workable for v1 maths, but back-testing and calibration are much harder.
- Python only (e.g. Streamlit): fine for prototypes, weak for a polished product UI.
- Microservices: unnecessary until real usage proves otherwise.
- Deep learning: football datasets are small and messy, and every adjustment must be explainable. Transparent statistical models come first.
