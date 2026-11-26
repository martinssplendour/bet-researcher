# Modularity Checklist

Use this checklist when reviewing code written by humans or agents.

## File Responsibility

- [ ] Each file has one clear responsibility.
- [ ] Each service has its own file.
- [ ] File names describe the concept they own.
- [ ] No file mixes unrelated workflows.
- [ ] No file mixes API routes, business logic, persistence, and external integrations.

## Service Boundaries

- [ ] Services coordinate use cases.
- [ ] Services do not directly own HTTP request/response formatting.
- [ ] Services do not hide database queries that belong in repositories.
- [ ] Services do not directly own provider-specific API details that belong in integrations.

## Utility Boundaries

- [ ] Generic `utils` or `helpers` files are small and genuinely generic.
- [ ] Business logic is not placed in generic helper files.
- [ ] Unrelated helper functions are split into named files.

## Split Triggers

Split the file if any answer is yes:

- [ ] Is the file hard to describe with one noun?
- [ ] Does the file contain more than one service?
- [ ] Does the file contain unrelated functions?
- [ ] Do tests for this file require unrelated fixtures?
- [ ] Would changing one feature risk breaking another unrelated feature?

## Review Result

- [ ] Approved.
- [ ] Needs splitting before merge.

