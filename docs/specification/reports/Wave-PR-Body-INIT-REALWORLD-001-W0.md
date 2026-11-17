# INIT-REALWORLD-001 W0 — Seat + public bulletin + feed order + prove scaffold

## Summary

- Register creates eligibility only (empty seat token); login remains the sole seat issuer
- Guest bulletin list/get/tag/profile reads stay ungated; global feed orders by `updated_at DESC, created_at DESC`
- Unseated contribution create fails closed without bearer (chassis 403); ADR-004 client JWT discard documented
- Co-shipped `make check`, `tests/README.md`, live verify driver + CAP/J fixtures for human wave-acceptance

## Initiative / tracking

- Initiative: INIT-REALWORLD-001
- Wave issue: https://github.com/drivestream-lab/realworld-api/issues/8
- Spec: `docs/specification/product/INIT-REALWORLD-001-api.md`
- Pre-implement: `docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md`
- Wave execution: `docs/specification/reports/Wave-Execution-INIT-REALWORLD-001-W0.md`

## Test plan

- [x] `make check`
- [x] `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (host: `DATABASE_URL` + plugin isolation; app coverage 100%)
- [ ] Human live: `poetry run python -m tests.verify.verify_wave0_seat_bulletin`
- [ ] Look-ats: newest-first feed JSON; deny publish after bearer omit
- [ ] Label tip `wave-accepted` when prove complete
