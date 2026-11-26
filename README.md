# Bet Researcher

Football bet research. A user pastes their picks or drops a screenshot of a bet slip, and the app researches every game: recent results, who scores the goals, who is missing, team news. It then explains, in plain language, how likely each pick is to win and how likely the whole ticket is to win.

Research, not betting advice.

## How it works

Each match goes through the same steps, every time:

1. Pull match data (results, players, injuries, odds) from API-Football.
2. Work out each team's expected goals from its last 12 games, against this opponent.
3. Gemini searches the news, then adjusts those numbers within fixed limits and explains why.
4. Turn expected goals into the chance of every scoreline, then of each pick and the whole ticket.

The full method is in [docs/method.md](docs/method.md).

## Tech Stack

| Part | Stack |
| --- | --- |
| Engine (`apps/engine`) | Python 3.12, uv, Pydantic, pytest, ruff, mypy. FastAPI, httpx, SQLAlchemy and the Google Gemini SDK are added as their features are built. |
| Web (`apps/web`) | Next.js + TypeScript (not started yet) |

Why: [docs/decisions/001-tech-stack.md](docs/decisions/001-tech-stack.md).

## Repository Layout

```text
apps/engine/            Python analysis engine
apps/web/               Next.js website (later)
docs/                   Method, architecture, decisions, development guides
senior-project-pack/    Reference standards this project follows
```

## Local Setup

Prerequisites: Python 3.12+, git, and uv (`python -m pip install --user uv`).

```bash
cd apps/engine
python -m uv sync
```

Then copy `.env.example` to `.env` in the repository root and fill in the keys. Never commit `.env`.

## Environment Variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `APP_ENV` | no | `development`, `test` or `production` (default `development`) |
| `LOG_LEVEL` | no | `DEBUG`, `INFO`, `WARNING` or `ERROR` (default `INFO`) |
| `DATABASE_URL` | no | Database connection (default: local SQLite file) |
| `API_FOOTBALL_KEY` | yes | API-Football key |
| `API_FOOTBALL_BASE_URL` | no | API-Football base URL |
| `GEMINI_API_KEY` | yes | Google Gemini key |
| `GEMINI_MODEL` | yes | Gemini model name |

The engine refuses to start if a required variable is missing or invalid.

## Running Tests

```bash
cd apps/engine
python -m uv run pytest
```

Tests run with coverage and fail below 80%.

## Common Commands

Run from `apps/engine`:

| Task | Command |
| --- | --- |
| Tests + coverage | `python -m uv run pytest` |
| Lint | `python -m uv run ruff check .` |
| Format | `python -m uv run ruff format .` |
| Type check | `python -m uv run mypy` |
| Security scan | `python -m uv run bandit -r src` |

## Architecture

- [Architecture overview and module boundaries](docs/architecture/overview.md)
- [Decision records](docs/decisions/)
- [Testing strategy](docs/development/testing.md)
- [Project brief](docs/project-brief.md)

## Deployment

Not decided yet. Hosting will get its own decision record before the first deployment.
