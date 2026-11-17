# Tests — realworld-api

Feature map for INIT-REALWORLD-001 Wave0a. Live modules under `tests/verify/`
are human-run against realworld-local compose; they are not unit coverage SSOT.

## Commands

| Layer | Command |
|-------|---------|
| Static check | `make check` |
| Unit (in-process) | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` |
| Live W0 | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` |

## Feature map

| Capability / journey | Live verify | Fixtures | Unit / integration |
|----------------------|-------------|----------|--------------------|
| CAP-01 public bulletin | `tests/verify/verify_wave0_seat_bulletin.py` | `tests/fixtures/cap-01-bulletin/` | `tests/test_api/test_routes/test_articles.py`, `test_profiles.py` |
| CAP-02 contribution seat | same | `tests/fixtures/cap-02-seat/` | `tests/test_api/test_routes/test_registration.py`, `test_login.py` |
| J-01 guest feed | same | `tests/fixtures/j-01-guest-feed/` | guest list/get assertions |
| J-05 register → login | same | `tests/fixtures/j-05-register-login/` | register without seat token; login seats |
| J-07 / J-08 / J-11 / J-17 | same (covers marker) | cap-02 + look-ats | 401/403 mutate deny; guest reads after unseat |

## Notes

- Pytest ignores `tests/verify/`, `tests/debug/`, and `tests/e2e/` for `make test` / CI unit runs when those dirs exist.
- Live prove at wave-acceptance: run the W0 verify command, complete human look-ats (newest-first feed JSON; deny publish after bearer omit), then label `wave-accepted` on the tip.
