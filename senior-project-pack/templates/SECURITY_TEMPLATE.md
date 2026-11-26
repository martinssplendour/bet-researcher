# Security

## Supported Versions

| Version | Supported |
| --- | --- |
| main | Yes |

## Reporting A Vulnerability

Report security issues to:

- Email:
- Private issue tracker:

Do not open public issues for sensitive vulnerabilities.

## Security Controls

| Area | Control |
| --- | --- |
| Secrets | Stored outside source control |
| Authentication | Centralized and tested |
| Authorization | Explicit role or permission checks |
| Input validation | Validated at app boundaries |
| Logging | Sensitive values redacted |
| Dependencies | Scanned in CI |
| Admin actions | Auditable |

## Sensitive Data

Document any sensitive data processed by the system:

- Data type:
- Storage location:
- Retention period:
- Access rules:
- Deletion process:

## Required Security Tests

- [ ] Auth success path.
- [ ] Auth failure path.
- [ ] Authorization denial path.
- [ ] Input validation failures.
- [ ] Rate limit or abuse protection if public.

