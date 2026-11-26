# Pre-Commit Checklist

- [ ] Change is focused.
- [ ] New code follows one service per file.
- [ ] No file has become a dumping ground for unrelated functions.
- [ ] Business logic is not hidden in generic `utils` or `helpers` files.
- [ ] Code is formatted.
- [ ] Lint passes.
- [ ] Typecheck passes if applicable.
- [ ] Tests pass locally.
- [ ] New behavior has tests.
- [ ] Error paths are handled.
- [ ] Logs do not expose secrets.
- [ ] `.env.example` updated if config changed.
- [ ] Docs updated if behavior changed.
- [ ] No generated artifacts or local files are committed.
