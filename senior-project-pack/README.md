# Senior Project Pack

This pack is a reusable starting kit for new software projects. Use it before writing feature code so every project starts with clear structure, documentation, testing, security, deployment, and operational standards.

## How To Use

1. Read `PROJECT_KICKOFF_CHECKLIST.md`.
2. Pick the closest starter structure from `starter-structures/`.
3. Copy the relevant templates from `templates/` into the new project.
4. Copy useful snippets from `snippets/`.
5. Use the checklists in `checklists/` before commits, releases, and production deployment.

## Recommended Minimum For Every Project

Copy these into every serious project:

- `templates/PROJECT_BRIEF_TEMPLATE.md` as `docs/project-brief.md`
- `templates/README_TEMPLATE.md` as `README.md`
- `templates/AGENT_CODING_RULES_TEMPLATE.md` as `AGENT_CODING_RULES.md`
- `templates/ENV_EXAMPLE_TEMPLATE` as `.env.example`
- `templates/ADR_TEMPLATE.md` as `docs/decisions/001-initial-architecture.md`
- `templates/ARCHITECTURE_OVERVIEW_TEMPLATE.md` as `docs/architecture/overview.md`
- `templates/PR_TEMPLATE.md` as `.github/pull_request_template.md`
- `templates/TESTING_STRATEGY_TEMPLATE.md` as `docs/development/testing.md`
- `checklists/pre-commit-checklist.md`
- `checklists/modularity-checklist.md`
- `checklists/production-readiness-checklist.md`

## Project Levels

Use the smallest level that still protects the project.

| Level | Use When | Required Pack Items |
| --- | --- | --- |
| Small | Prototype, script, internal utility | README, `.env.example`, basic tests, pre-commit checklist |
| Standard | Real app or service | README, architecture overview, ADRs, tests, PR template, CI |
| Production | Customer-facing or business-critical | Standard plus deployment, monitoring, incident response, security checklist |
| Regulated/Data-Heavy | Sensitive data, AI, payments, healthcare, finance | Production plus data/artifact docs, evaluation, retention, audit trail |

## Senior Rule

Do not blindly create every file. Use the pack to make deliberate choices visible.
