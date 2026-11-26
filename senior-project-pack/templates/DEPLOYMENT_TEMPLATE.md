# Deployment

## Environments

| Environment | URL | Purpose | Owner |
| --- | --- | --- | --- |
| Development |  | Local/dev testing |  |
| Staging |  | Pre-production validation |  |
| Production |  | Customer traffic |  |

## Deployment Method

Describe how deployments happen:

- Platform:
- CI workflow:
- Artifact:
- Trigger:

## Required Configuration

| Name | Environment | Required | Notes |
| --- | --- | --- | --- |
| `APP_ENV` | All | Yes |  |

## Pre-Deploy Checklist

- [ ] Tests pass.
- [ ] Build succeeds.
- [ ] Migrations reviewed.
- [ ] Config changes applied.
- [ ] Rollback path confirmed.
- [ ] Monitoring checked.

## Deploy Steps

```bash
[deploy command or workflow]
```

## Post-Deploy Checks

- [ ] Health check passes.
- [ ] Error rate is normal.
- [ ] Logs show expected startup.
- [ ] Critical workflow works.

## Rollback

```bash
[rollback command or process]
```

## Known Risks

- 

