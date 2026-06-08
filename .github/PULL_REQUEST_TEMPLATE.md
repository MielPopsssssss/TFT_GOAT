## What & why

<!-- Short description of the change and the motivation. Link any issue: Closes #123 -->

## How I verified

```bash
python -m pytest -q
```

<!-- Paste relevant output / new test names. For game-data changes, link your source. -->

## Checklist

- [ ] Tests pass locally (`python -m pytest -q`)
- [ ] New behavior has a test
- [ ] Real data used as source of truth (no hand-typed numbers)
- [ ] `docs/COMBAT_COVERAGE.md` updated if combat fidelity changed
- [ ] Conventional commit message (`feat:`, `fix:`, `docs:`, ...)
