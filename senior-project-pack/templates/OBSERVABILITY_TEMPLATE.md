# Observability

## Goals

The system should make production behavior understandable without code changes.

## Logs

Required log fields:

- Timestamp
- Level
- Service name
- Request ID or correlation ID
- User or tenant ID if safe
- Operation name
- Error code if applicable

Sensitive values that must never be logged:

- Passwords
- Tokens
- API keys
- Payment data
- Private user data unless explicitly approved

## Metrics

| Metric | Type | Why It Matters |
| --- | --- | --- |
| Request count | Counter | Traffic |
| Error count | Counter | Failure rate |
| Request latency | Histogram | User experience |
| Queue depth | Gauge | Backlog |
| External API latency | Histogram | Dependency health |

## Traces

Trace these flows:

- Critical user workflow:
- Payment or billing workflow:
- Background job:
- External API call:

## Dashboards

Required dashboards:

- Service overview
- Error rate and latency
- Database or storage health
- External dependency health
- Business-critical workflow health

## Alerts

| Alert | Trigger | Severity | Owner |
| --- | --- | --- | --- |
| High error rate |  |  |  |
| High latency |  |  |  |
| Failed background jobs |  |  |  |
| Low disk/storage |  |  |  |

## Runbook Links

- Deployment:
- Rollback:
- Incident response:
- Logs:
- Dashboard:

