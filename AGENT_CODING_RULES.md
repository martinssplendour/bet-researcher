# Agent Coding Rules

Instructions for AI coding agents and human contributors. Adapted from `senior-project-pack/templates/AGENT_CODING_RULES_TEMPLATE.md` for this project.

## Core Rules

- **One responsibility per file.** One service per file. No `helpers.py`, `utils.py`, `services.py` or other dumping grounds.
- **Name files after the concept they own:** `history_window.py`, `scoreline_model.py`, `api_football_client.py`.
- **Tests first.** Write the failing test, then the code, then refactor. Coverage must stay at or above 80%.
- **Immutable data.** Frozen dataclasses and tuples. Return new objects; never change inputs.
- **Type annotations on every function.** `mypy --strict` must pass.
- **No `print()`.** Use the `logging` module.
- **No secrets in code.** Read them from settings, which load from `.env`.

## Where Code Goes (engine)

```text
apps/engine/src/bet_researcher/
|-- core/           settings, logging, error types
|-- domain/         pure maths and rules: no I/O, no network, no database
|-- integrations/   API-Football and Gemini clients only
|-- repositories/   reading and saving stored data only
|-- services/       one workflow per file, e.g. match_analysis_service.py
|-- prompts/        versioned Gemini prompts
`-- api/            thin HTTP routes (later)
```

| Folder | May import | Must not |
| --- | --- | --- |
| `domain/` | `core/errors`, standard library | do I/O, call APIs, read settings |
| `integrations/` | `core/`, `domain/` types | contain business rules |
| `repositories/` | `core/`, `domain/` types | call external APIs |
| `services/` | everything above | contain HTTP or SQL details |
| `api/` | `services/` | contain business logic |

## Project-Specific Rules

These come from [docs/method.md](docs/method.md):

- **Code does every calculation.** Gemini never produces the core numbers. It proposes capped adjustments with reasons.
- **Every adjustment is capped** (default ±30%) by code, whatever Gemini returns.
- **Every number in Gemini's text must exist in the fact sheet.** Code checks and rejects text that fails.
- **Picks on the same match are worked out together** from that match's scoreline table, never multiplied.
- **Every tunable number** (window size, weights, caps, thresholds) is a named constant or config value, never a magic number.
- **Validate at the edges.** API responses and user input are checked with Pydantic before reaching the domain.

## Split File Triggers

Split a file when it holds more than one service, mixes API, business logic and storage, becomes hard to name with one noun, or passes roughly 400 lines.

## Review Checklist

- [ ] Each file has one clear responsibility.
- [ ] Domain code has no I/O.
- [ ] Tests were written first and cover failure cases.
- [ ] No magic numbers; tunable values are named.
- [ ] No secrets, no `print()`.
- [ ] `ruff check`, `ruff format --check`, `mypy` and `pytest` all pass.
