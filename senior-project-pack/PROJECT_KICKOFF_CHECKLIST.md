# Project Kickoff Checklist

Use this before building the first feature.

## Product Clarity

- [ ] Project purpose is written in one paragraph.
- [ ] Target users are identified.
- [ ] Primary user workflows are listed.
- [ ] Non-goals are listed.
- [ ] Success criteria are defined.

## Technical Shape

- [ ] Tech stack is chosen and justified.
- [ ] Runtime and package manager versions are defined.
- [ ] Repository structure is selected from `starter-structures/`.
- [ ] Main module boundaries are documented.
- [ ] Agent coding rules are copied into the project.
- [ ] One-service-per-file rule is accepted for the project.
- [ ] External systems and dependencies are listed.
- [ ] Data storage choice is documented.
- [ ] Authentication and authorization strategy is documented if needed.

## Developer Experience

- [ ] `README.md` exists.
- [ ] `.env.example` exists.
- [ ] Local setup command is documented.
- [ ] Test command is documented.
- [ ] Common scripts are documented.
- [ ] Formatting and linting commands are documented.

## Quality

- [ ] Unit test structure exists.
- [ ] Integration test structure exists if external systems are used.
- [ ] E2E test plan exists if user workflows matter.
- [ ] Error handling strategy is defined.
- [ ] Logging strategy is defined.
- [ ] Configuration validation exists or is planned.

## Delivery

- [ ] CI test workflow exists.
- [ ] Build process is documented.
- [ ] Deployment target is documented.
- [ ] Rollback path is documented if production-bound.
- [ ] Monitoring and alerting needs are identified.

## Governance

- [ ] First ADR exists.
- [ ] PR template exists.
- [ ] Security checklist is reviewed.
- [ ] Secrets handling is defined.
- [ ] Data/artifact storage rules are defined.
