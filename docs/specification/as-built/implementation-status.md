# Implementation status (index)

One row per capability. Overwrite in place; never append a second table.
Detail: open the cited `Implementation-Status-{INIT}.md`.

## Testing harness

| Layer | Command / path |
|-------|----------------|
| Check | `make check` |
| Unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` |
| Live verify | `tests/verify/` (per-wave modules; see `tests/README.md`) |
| Fixtures | `tests/fixtures/` |

## Capability index

| Capability | Initiative | Wave | Status | human_approved | Detail |
|------------|------------|------|--------|----------------|--------|
| CAP-01 public bulletin | INIT-REALWORLD-001 | W0 | implemented / unit-tested / live-verified | yes (wave-acceptance PR #25) | `Implementation-Status-INIT-REALWORLD-001.md` |
| CAP-02 contribution seat | INIT-REALWORLD-001 | W0 | implemented / unit-tested / live-verified | yes (wave-acceptance PR #25) | `Implementation-Status-INIT-REALWORLD-001.md` |
| CAP-03 tagged publish | INIT-REALWORLD-001 | W1 | planned | no | `Implementation-Status-INIT-REALWORLD-001.md` |
| CAP-04 own revise/delete | INIT-REALWORLD-001 | W1 | planned | no | `Implementation-Status-INIT-REALWORLD-001.md` |
| CAP-05 private shelf | INIT-REALWORLD-001 | W2 | planned | no | `Implementation-Status-INIT-REALWORLD-001.md` |
| CAP-06 nameplate | INIT-REALWORLD-001 | W2 | planned | no | `Implementation-Status-INIT-REALWORLD-001.md` |
