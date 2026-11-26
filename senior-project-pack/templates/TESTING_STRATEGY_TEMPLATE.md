# Testing Strategy

## Test Commands

```bash
# all tests
[command]

# unit tests
[command]

# integration tests
[command]

# e2e tests
[command]
```

## Test Levels

| Level | Purpose | Required For |
| --- | --- | --- |
| Unit | Isolated rules/functions | Domain logic, validators, services |
| Integration | Real adapters and infrastructure | Database, queues, APIs, storage |
| E2E | User workflows | Critical product paths |
| Load | Throughput and latency | Production-facing services |

## Coverage Expectations

- Business rules are unit tested.
- Critical routes/workflows have integration or E2E coverage.
- Bug fixes include regression tests when practical.
- Auth and permission behavior is tested.
- Error paths are tested.

## Test Data

- Fixture location:
- Test database strategy:
- Data reset strategy:
- Secrets used in tests:

## What Not To Mock

List dependencies that should be exercised in integration tests.

## Release Gate

A release is blocked if:

- Critical tests fail.
- Migrations cannot be verified.
- Security-critical paths are untested.
- Production rollback is unclear.

