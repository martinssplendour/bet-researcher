# [Project Name]

## Purpose

Describe what this project does, who it is for, and what problem it solves.

## Status

- Stage: [prototype | development | staging | production]
- Owner: [team/person]
- Last reviewed: [YYYY-MM-DD]

## Tech Stack

- Language:
- Framework:
- Database:
- Cache:
- Queue:
- Deployment:
- Observability:

## Local Setup

```bash
# install dependencies
[command]

# copy environment file
cp .env.example .env

# run locally
[command]
```

## Environment Variables

See `.env.example`.

Important variables:

| Name | Required | Purpose |
| --- | --- | --- |
| `APP_ENV` | Yes | Runtime environment |
| `DATABASE_URL` | If database is used | Database connection |
| `LOG_LEVEL` | Yes | Logging level |

## Common Commands

```bash
# run app
[command]

# run tests
[command]

# lint
[command]

# build
[command]
```

## Architecture

Read:

- `docs/architecture/overview.md`
- `docs/architecture/system-context.md`
- `docs/architecture/module-boundaries.md`
- `docs/decisions/`

## Testing

Describe test levels and commands.

```bash
[test command]
```

## Deployment

Read `docs/operations/deployment.md`.

## Security

Read `SECURITY.md` or `docs/operations/security.md`.

## Troubleshooting

| Problem | Likely Cause | Fix |
| --- | --- | --- |
| App will not start | Missing env vars | Compare `.env` with `.env.example` |

