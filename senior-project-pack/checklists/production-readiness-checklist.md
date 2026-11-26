# Production Readiness Checklist

## Runtime

- [ ] App starts from a clean environment.
- [ ] Required config is validated at startup.
- [ ] Health check exists.
- [ ] Readiness check exists if needed.
- [ ] Graceful shutdown is handled if applicable.

## Reliability

- [ ] Critical workflows have tests.
- [ ] External dependency failures are handled.
- [ ] Retries and timeouts are defined.
- [ ] Background jobs are observable if used.
- [ ] Database migrations are reversible or safely forward-only.

## Observability

- [ ] Structured logs exist.
- [ ] Request IDs or correlation IDs exist.
- [ ] Error tracking is configured.
- [ ] Metrics exist for traffic, latency, errors, and saturation.
- [ ] Alerts exist for critical failures.

## Security

- [ ] Secrets are not committed.
- [ ] Auth and authorization are tested.
- [ ] Sensitive data handling is documented.
- [ ] Dependency scanning is active.
- [ ] Rate limits exist where needed.

## Operations

- [ ] Deployment process is documented.
- [ ] Rollback process is documented.
- [ ] Incident response doc exists.
- [ ] Backup and restore are defined if data is stored.
- [ ] Ownership is clear.

