# Security Checklist

## Secrets

- [ ] No real secrets in source control.
- [ ] `.env.example` contains names only, not values.
- [ ] Production secrets are stored in a secret manager or platform config.

## Authentication

- [ ] Auth is centralized.
- [ ] Session/token expiration is defined.
- [ ] Failed auth paths are tested.

## Authorization

- [ ] Protected actions have explicit permission checks.
- [ ] Admin-only operations are tested.
- [ ] Object ownership checks exist where needed.

## Input And Output

- [ ] Inputs are validated at boundaries.
- [ ] Error messages do not leak sensitive details.
- [ ] Sensitive logs are redacted.

## Dependencies

- [ ] Dependency scanning exists.
- [ ] Unused dependencies are removed.
- [ ] Dangerous packages are reviewed before use.

## Abuse Protection

- [ ] Public endpoints have rate limits if needed.
- [ ] Expensive operations have limits.
- [ ] File uploads have size and type restrictions if used.

