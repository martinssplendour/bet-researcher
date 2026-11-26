# Testing Strategy

## Rules

- Tests first: write the failing test, then the code.
- Coverage of at least 80%, enforced by pytest (`--cov-fail-under=80`).
- Test failure cases, not only happy paths.
- Bug fixes come with a regression test.

## Levels

| Level | Where | What | Marker |
| --- | --- | --- | --- |
| Unit | `apps/engine/tests/unit/` | Domain maths and rules; settings. No I/O. | `unit` |
| Integration | `apps/engine/tests/integration/` | API-Football and Gemini clients against recorded responses (respx); repositories against PostgreSQL (Docker) | `integration` |
| Evaluation | `apps/engine/tests/evals/` | Gemini prompt behaviour on fixed fact sheets (later) | `eval` |
| E2E | `apps/web` (Playwright) | Paste ticket → analysing → results (later) | n/a |

## Known-answer tests

Domain maths is checked against hand-calculated values from the method's worked example. For example, expected goals of 2.1 and 0.9 give a home win near 65%, a draw near 20%, and home win plus over 2.5 goals near 44%.

## Commands

```bash
cd apps/engine
python -m uv run pytest              # all tests with coverage
python -m uv run pytest -m unit      # unit tests only
```
