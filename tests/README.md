# Tests — realworld-api

## Layers

| Layer | Command | Role |
|-------|---------|------|
| Check | `make check` | Black format gate (`app/`, `tests/`) |
| Unit / in-process | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | Fast assertions; no live compose |
| Live verify | Wave-scoped modules under `tests/verify/` | Human smoke against running API + fixtures |

Live verify is **not** a coverage SSOT. Fixture packs live under `tests/fixtures/`.

## Feature map (INIT-REALWORLD-001)

| Capability / journey | Wave | Live module | Fixtures |
|----------------------|------|-------------|----------|
| CAP-01 public bulletin + J-01 guest feed | W0 | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` | `tests/fixtures/cap-01-bulletin/`, `tests/fixtures/j-01-guest-feed/` |
| CAP-02 contribution seat + J-05 register/login | W0 | same | `tests/fixtures/cap-02-seat/`, `tests/fixtures/j-05-register-login/` |
| CAP-03 publish / revise | W1 | `poetry run python -m tests.verify.verify_wave1_publish_revise` | (W1) |
| CAP-05 / CAP-06 shelf + nameplate | W2 | `poetry run python -m tests.verify.verify_wave2_shelf_nameplate` | (W2) |

## Prerequisites for live verify

- `realworld-local` compose up; API reachable (see product plan)
- Synthetic users/articles only; follow each fixture pack `cleanup.md`
