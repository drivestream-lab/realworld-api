# Wave execution — INIT-REALWORLD-001 W0

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-001 |
| Wave | W0 |
| Wave head context | Bound by Forge/human: `feature/init-realworld-001-w0-realworld-api` |
| Board wave issue | https://github.com/drivestream-lab/realworld-api/issues/8 |
| WorkManifest source | plan §9 (immutable intent — not mutated) |
| Outcome | pass |

## Completed TASKS

| TASK | Implements | Declared files | Proof expected (manifest) | Observed (command / evidence) | Status |
|------|------------|----------------|---------------------------|-------------------------------|--------|
| TASK-W0-01 | REQ-01 | `Makefile`; `tests/README.md` | `make check` → exit 0 | `make check` → exit 0 (black --check app tests) | green |
| TASK-W0-02 | REQ-08, REQ-09, REQ-10, REQ-11 | `app/api/routes/authentication.py`; `tests/test_api/test_routes/test_registration.py`; `tests/test_api/test_routes/test_login.py` | pytest seat assertions | register returns `token=""`; login returns non-empty token; duplicate/bad login 400; `make check` + unit exit 0 | green |
| TASK-W0-03 | REQ-01..07, REQ-12..14, REQ-34 | `app/db/repositories/articles.py`; `app/api/routes/articles/articles_resource.py`; `tests/test_api/test_routes/test_articles.py`; `tests/test_api/test_routes/test_profiles.py` | guest reads + order + deny | `filter_articles` `ORDER BY updated_at DESC, created_at DESC`; guest list/get/tag/author 200; unseated create **403** (APIKeyHeader fail-closed); ADR-004 comment on articles router; check+unit exit 0 | green |
| TASK-W0-04 | REQ-01..14, REQ-34 | `tests/verify/*`; `tests/fixtures/cap-01-bulletin/*`; `tests/fixtures/cap-02-seat/*`; `tests/fixtures/j-01-guest-feed/stimulus.json`; `tests/fixtures/j-05-register-login/stimulus.json` | live module + covers | Files created with `prayog:covers:` CAP-01/CAP-02 + J-*; **did not** run live smoke as loop-spec success; check+unit exit 0 | green |

## Unit evidence notes

- Host unit command used project `.venv`, `DATABASE_URL=postgresql://adh:adh@localhost:5432/realworld`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` (ROS launch_testing plugin otherwise breaks collection), and `-o addopts=... --cov=app ...` so assert-rewrite under `--cov=tests` does not false-fail the 100% gate. App line/branch coverage observed **100%**; **95 passed**.
- Final wave gate after TASK-W0-04: `make check` exit 0; unit exit 0.

## Live verify (human — not claimed here)

- Planned script: `poetry run python -m tests.verify.verify_wave0_seat_bulletin` under `tests/verify`
- Prove rungs: CAP-01, CAP-02 / J-01, J-05, J-07, J-08, J-11, J-17
- Fixtures: `tests/fixtures/cap-01-bulletin/`, `tests/fixtures/cap-02-seat/`, `tests/fixtures/j-01-guest-feed/`, `tests/fixtures/j-05-register-login/`
- Look-ats: API JSON feed order + deny after bearer omit — newest-first slugs; deny on publish (chassis may return 403; product fail-closed)
- Agent created planned FILE + fixtures: **yes** — **did not** run smoke/sandbox or claim look-at success
- Evidence expected for human accept: `wave-accepted` on tip

## Forge readiness

- After this hop: `commit_workspace` (code on bound `head_ref`)
- Next external-action: `open_draft_pr` / `wave-pr-action`
  - title: `INIT-REALWORLD-001 W0 — Seat + public bulletin + feed order + prove scaffold`
  - body_path: `docs/specification/reports/Wave-PR-Body-INIT-REALWORLD-001-W0.md`
  - head_ref: `feature/init-realworld-001-w0-realworld-api`
  - base_ref: `develop`

## Human prove checklist (wave-acceptance)

1. Ensure wave tip is running against realworld-local compose (redeploy API with this head).
2. Run `poetry run python -m tests.verify.verify_wave0_seat_bulletin`.
3. Complete look-ats (newest-first; unseated publish denied).
4. Apply GitHub label `wave-accepted` on the Draft PR tip.

---

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: loop-spec
  outcome: pass
  artifact:
    path: docs/specification/reports/Wave-Execution-INIT-REALWORLD-001-W0.md
  blockers: []
  signals:
    initiative: INIT-REALWORLD-001
    wave: W0
    wave_issue: https://github.com/drivestream-lab/realworld-api/issues/8
    current_task: null
    implements:
      - REQ-01
      - REQ-02
      - REQ-03
      - REQ-04
      - REQ-05
      - REQ-06
      - REQ-07
      - REQ-08
      - REQ-09
      - REQ-10
      - REQ-11
      - REQ-12
      - REQ-13
      - REQ-14
      - REQ-34
    completed_tasks:
      - TASK-W0-01
      - TASK-W0-02
      - TASK-W0-03
      - TASK-W0-04
    check_command: make check
    test_command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
    verify_command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
    live_covers:
      - CAP-01
      - CAP-02
      - J-01
      - J-05
      - J-07
      - J-08
      - J-11
      - J-17
    fixtures:
      - tests/fixtures/cap-01-bulletin/
      - tests/fixtures/cap-02-seat/
      - tests/fixtures/j-01-guest-feed/
      - tests/fixtures/j-05-register-login/
    human_observations:
      - locus: API JSON feed order + deny after bearer omit
        expect: newest-first slugs; deny on publish
        covers: [CAP-01, CAP-02]
    head_ref: feature/init-realworld-001-w0-realworld-api
    integration_branch: develop
    live_verify_executed_by_loop_spec: false
  next_candidates:
    - wave-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels: []
    remove_labels: []
    title: "INIT-REALWORLD-001 W0 — Seat + public bulletin + feed order + prove scaffold"
    body_path: docs/specification/reports/Wave-PR-Body-INIT-REALWORLD-001-W0.md
    head_ref: feature/init-realworld-001-w0-realworld-api
    base_ref: develop
```
