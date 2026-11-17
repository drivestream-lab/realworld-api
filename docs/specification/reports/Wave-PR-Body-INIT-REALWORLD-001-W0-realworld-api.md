## Summary

- INIT-REALWORLD-001 W0: seat lifecycle (register ≠ seat; login seats), ungated public bulletin reads, newest-first feed order (REQ-34), and co-shipped live verify/fixtures for CAP-01 / CAP-02.
- Wave head: `feature/init-realworld-001-w0-realworld-api` ← `develop`.
- Local proof: `make check` + unit pytest green; live smoke is **human** at wave-acceptance.

## Initiative / Spec

- **Initiative:** INIT-REALWORLD-001
- **Spec path:** `docs/specification/product/INIT-REALWORLD-001-api.md`
- **Wave:** W0 — Seat + public bulletin + feed order + prove scaffold
- **Board:** https://github.com/drivestream-lab/realworld-api/issues/8

## Smoke / Verify (human)

```bash
poetry run python -m tests.verify.verify_wave0_seat_bulletin
```

Covers: CAP-01, CAP-02, J-01, J-05, J-07, J-08, J-11, J-17. Fixtures under `tests/fixtures/cap-01-bulletin/`, `cap-02-seat/`, `j-01-guest-feed/`, `j-05-register-login/`. Look-at: API JSON feed order + 401/403 after bearer omit.

## Test plan

- [x] `make check`
- [x] `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/`
- [ ] Human live verify (command above) + look-ats → label `wave-accepted`
