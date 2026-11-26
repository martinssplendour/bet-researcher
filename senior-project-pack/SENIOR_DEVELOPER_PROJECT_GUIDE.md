# Senior Developer Project Guide

Use this guide at the start of every serious project. Its purpose is to make the project understandable, testable, deployable, secure, and maintainable from day one.

This is not a folder-template-only document. It is a working standard for how to think, structure, document, and ship software at a senior level.

## 1. Project Start Rule

Before writing feature code, define these five things:

1. What problem the system solves.
2. Who uses it.
3. What the main workflows are.
4. What the system depends on.
5. How the system will be tested, deployed, monitored, and changed safely.

If these are unclear, create a short `docs/architecture/overview.md` before building.

## 2. Baseline Repository Structure

Use this as the default starting point. Adjust names to the language or framework, but keep the responsibilities clear.

```text
project_root/
|-- README.md
|-- .gitignore
|-- .env.example
|-- pyproject.toml / package.json / go.mod / Cargo.toml
|-- docs/
|   |-- index.md
|   |-- getting-started.md
|   |-- architecture/
|   |   |-- overview.md
|   |   |-- system-context.md
|   |   |-- request-lifecycle.md
|   |   |-- data-flow.md
|   |   `-- module-boundaries.md
|   |-- api/
|   |   |-- openapi.yaml
|   |   `-- authentication.md
|   |-- development/
|   |   |-- local-setup.md
|   |   |-- testing.md
|   |   |-- code-style.md
|   |   `-- contributing.md
|   |-- operations/
|   |   |-- deployment.md
|   |   |-- configuration.md
|   |   |-- monitoring.md
|   |   `-- incident-response.md
|   `-- decisions/
|       |-- 001-database-choice.md
|       |-- 002-auth-design.md
|       `-- 003-deployment-strategy.md
|-- src/ or app/
|   |-- api/
|   |-- services/
|   |-- domain/
|   |-- repositories/
|   |-- integrations/
|   |-- core/
|   `-- main.*
|-- tests/
|   |-- unit/
|   |-- integration/
|   |-- e2e/
|   `-- load/
|-- scripts/
|-- config/
|   |-- development.example.yaml
|   |-- staging.example.yaml
|   `-- production.example.yaml
|-- deployment/
|   |-- Dockerfile
|   |-- docker-compose.yml
|   |-- kubernetes/
|   `-- nginx/
|-- monitoring/
|   |-- dashboards/
|   |-- alerts/
|   `-- metrics/
`-- .github/
    `-- workflows/
        |-- test.yml
        |-- build.yml
        `-- deploy.yml
```

## 3. Responsibility Boundaries

Keep these boundaries clean:

| Area | Responsibility |
| --- | --- |
| `api/` | HTTP routes, request parsing, response formatting, auth entry points |
| `services/` | Application workflows and business use cases |
| `domain/` or `models/` | Core entities, rules, state, validation |
| `repositories/` | Database access and persistence contracts |
| `integrations/` | External APIs, queues, storage, email, payment, AI providers |
| `core/` | Config, logging, errors, dependency wiring, security helpers |
| `utils/` | Small generic helpers only; avoid hiding business logic here |
| `scripts/` | Repeatable developer or operational commands |
| `docs/` | How the system works and how to safely change it |

Senior rule: business logic should not live in routes, controllers, random helpers, notebooks, or deployment scripts.

## 4. README Standard

Every project needs a `README.md` that answers:

1. What is this project?
2. What problem does it solve?
3. How do I run it locally?
4. How do I run tests?
5. What environment variables are required?
6. What services does it depend on?
7. Where are the architecture docs?
8. How is it deployed?

Minimum README outline:

```markdown
# Project Name

## Purpose

## Tech Stack

## Local Setup

## Environment Variables

## Running the App

## Running Tests

## Architecture

## Deployment

## Common Commands
```

## 5. Architecture Documentation Standard

Architecture docs should explain decisions, boundaries, and system behavior. They should not simply repeat the folder tree.

Required architecture docs:

- `overview.md`: high-level system purpose, users, main workflows.
- `system-context.md`: external systems, dependencies, data sources, APIs.
- `request-lifecycle.md`: what happens when a user or client sends a request.
- `data-flow.md`: how data enters, moves through, and leaves the system.
- `module-boundaries.md`: what each major module owns and must not own.

Good architecture docs answer:

- Why is the system shaped this way?
- What can change independently?
- Where do failures happen?
- What must be protected?
- What are the scaling limits?
- What tradeoffs were accepted?

## 6. Architecture Decision Records

Use ADRs for decisions that future developers should not have to rediscover.

Create an ADR when choosing:

- Database
- Auth strategy
- Deployment platform
- Queue or event system
- Vector store
- AI provider
- Payment provider
- Caching strategy
- Major framework
- Data retention policy

ADR template:

```markdown
# ADR 001: Decision Title

## Status

Accepted

## Context

What problem are we solving?

## Decision

What did we choose?

## Consequences

What improves?
What gets worse?
What must future developers know?

## Alternatives Considered

What else did we evaluate?
```

## 7. Configuration Standard

Never commit real secrets.

Use:

- `.env.example` for required environment variables.
- `config/*.example.yaml` for environment-specific configuration examples.
- Secret managers for real production values.
- Runtime validation for required config.

Required config categories:

- App environment
- Database URL
- Auth secrets
- External API keys
- Storage credentials
- Logging level
- Feature flags
- Rate limits
- Model/provider config if using AI

Senior rule: the app should fail fast on invalid configuration.

## 8. Testing Standard

Default test structure:

```text
tests/
|-- unit/
|-- integration/
|-- e2e/
`-- load/
```

Use each level correctly:

| Test Type | Purpose |
| --- | --- |
| Unit | Test isolated functions, entities, services, and rules |
| Integration | Test database, queues, external service adapters, file storage |
| E2E | Test real user workflows through the app boundary |
| Load | Test throughput, latency, memory, and failure behavior |

Minimum quality bar:

- Core business rules have unit tests.
- Critical API routes have integration or E2E tests.
- Authentication and authorization paths are tested.
- Failure cases are tested, not only happy paths.
- Bug fixes include regression tests when practical.

## 9. CI/CD Standard

Every project should have a pipeline like this:

```text
Commit
  -> Lint
  -> Typecheck
  -> Tests
  -> Build
  -> Security Scan
  -> Deploy
```

Minimum workflows:

- `test.yml`: lint, format check, typecheck, unit tests.
- `build.yml`: build package/container/app artifact.
- `deploy.yml`: deploy to staging or production.

Deployment should be repeatable. A developer should not need tribal knowledge or manual steps to ship.

## 10. Security Standard

Security should be designed into the project structure, not added later.

Required security checks:

- Authentication is centralized.
- Authorization is explicit and testable.
- Secrets are never committed.
- Inputs are validated at boundaries.
- Database access uses parameterized queries or ORM-safe APIs.
- Sensitive logs are redacted.
- Admin operations are auditable.
- Dependencies are scanned.
- Rate limits exist for public or expensive endpoints.

Do not create a root `security/` code folder unless security is its own package. Prefer placing application security code near the app core, for example:

```text
app/core/security.py
app/api/auth.py
app/services/authorization_service.py
```

Use `docs/operations/security.md` or `docs/api/authentication.md` for security documentation.

## 11. Observability Standard

Every production-grade project needs visibility.

Include:

- Structured logs
- Request IDs or correlation IDs
- Metrics for latency, errors, throughput, and saturation
- Health checks
- Alerts
- Dashboards
- Error tracking

Minimum production health endpoints:

- `/health`: process is alive.
- `/ready`: app can serve traffic.
- `/metrics`: metrics endpoint, if applicable.

Senior rule: if production fails, the system should help you diagnose it.

## 12. Data And Artifact Standard

Avoid committing large generated data, embeddings, model checkpoints, user uploads, or build artifacts.

Use the repo for:

- Schemas
- Migration scripts
- Small fixtures
- Data contracts
- Example inputs

Use external storage for:

- Raw datasets
- Processed datasets
- Embeddings
- Trained models
- Checkpoints
- User-generated files

If the project is data-heavy, document:

- Data source
- Data owner
- Data format
- Retention rules
- Privacy constraints
- Regeneration process
- Backup and restore process

## 13. API Standard

Every API project should document:

- Routes
- Request bodies
- Response bodies
- Error format
- Auth requirements
- Rate limits
- Pagination
- Versioning

Prefer an OpenAPI spec:

```text
docs/api/openapi.yaml
```

Standard error shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request is invalid.",
    "details": []
  }
}
```

## 14. Pull Request Standard

Every pull request should answer:

1. What changed?
2. Why did it change?
3. How was it tested?
4. What risks remain?
5. Are migrations, config, or deployment changes required?

PR checklist:

- Tests added or updated.
- Docs updated if behavior changed.
- Config changes documented.
- Security impact considered.
- Backward compatibility considered.
- Observability updated if needed.

## 15. Definition Of Done

A feature is not done just because it works locally.

Done means:

- Code is implemented.
- Tests pass.
- Edge cases are handled.
- Errors are understandable.
- Logs and metrics exist where needed.
- Docs are updated.
- Config is documented.
- Deployment impact is understood.
- Security impact is reviewed.

## 16. Optional AI / LLM Project Structure

For AI-heavy systems, add these modules only when needed:

```text
app/
|-- services/
|   |-- llm_service.py
|   |-- embedding_service.py
|   |-- vector_search_service.py
|   `-- speech_service.py
|-- integrations/
|   |-- openai_client.py
|   |-- vector_store_client.py
|   `-- speech_provider_client.py
|-- evaluation/
|   |-- datasets/
|   |-- evaluators/
|   `-- reports/
`-- prompts/
    |-- system/
    |-- user/
    `-- versions/
```

AI-specific docs:

```text
docs/ai/
|-- model-selection.md
|-- prompt-strategy.md
|-- evaluation.md
|-- safety.md
`-- cost-controls.md
```

AI-specific senior checks:

- Prompt versions are tracked.
- Model choices are documented.
- Evaluations exist for important workflows.
- Token/cost limits are configured.
- User data handling is documented.
- Retrieval quality can be tested.
- Fallback behavior is defined.

## 17. New Project Kickoff Checklist

Use this checklist whenever starting a new project.

```markdown
## Project Kickoff Checklist

- [ ] Purpose is documented.
- [ ] Target users are documented.
- [ ] Main workflows are listed.
- [ ] Tech stack is chosen.
- [ ] Repository structure is created.
- [ ] README exists.
- [ ] `.env.example` exists.
- [ ] Architecture overview exists.
- [ ] Module boundaries are documented.
- [ ] First ADR is created.
- [ ] Test structure exists.
- [ ] CI test workflow exists.
- [ ] Deployment path is documented.
- [ ] Config strategy is documented.
- [ ] Logging strategy is defined.
- [ ] Security basics are defined.
- [ ] Data/artifact storage strategy is defined.
- [ ] PR checklist is defined.
```

## 18. Senior Developer Mindset

Start every project with these habits:

- Make the system easy to understand.
- Make the system easy to run.
- Make the system easy to test.
- Make the system easy to deploy.
- Make the system easy to observe.
- Make failure modes visible.
- Keep boundaries clear.
- Record decisions before they become mysteries.
- Prefer repeatable commands over manual steps.
- Keep secrets, data, and generated artifacts out of source control.

The goal is not to make every project large. The goal is to make every project professionally shaped from the beginning.
