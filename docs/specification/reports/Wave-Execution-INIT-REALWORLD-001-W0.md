# Wave execution — INIT-REALWORLD-001 W0

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-001 |
| Wave | W0 |
| Wave head context | Bound by Forge/human: `feature/init-realworld-001-w0-realworld-api` (from `develop`) |
| Board wave issue | https://github.com/drivestream-lab/realworld-api/issues/8 |
| WorkManifest source | plan §9 (immutable intent — not mutated) |
| Pre-implement | `docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md` — Gate verdict PASS |
| Outcome | pass |

## Completed TASKS

| TASK | Implements | Declared files | Proof expected (manifest) | Observed (command / evidence) | Status |
|------|------------|----------------|---------------------------|-------------------------------|--------|
| TASK-W0-01 | REQ-01 | `Makefile`; `tests/README.md` | `make check` exit 0 | `make check` → exit 0 (black --check app tests); unit pytest 95 passed | green |
| TASK-W0-02 | REQ-08, REQ-09, REQ-10, REQ-11 | `app/api/routes/authentication.py`; registration/login tests | register/login seat rules via pytest | Register returns empty token; login returns token; duplicate/invalid fail-closed; `make check` + pytest exit 0 | green |
| TASK-W0-03 | REQ-01..07, REQ-12..14, REQ-34 | articles repo/resource; articles/profiles tests | guest reads + order + unseated mutate deny | Guest list/get/tag/profile 200; ORDER BY `updated_at DESC, created_at DESC`; unseated create **403** (chassis APIKeyHeader — fail-closed; plan text said 401); ADR-004 discard note on articles resource; check+pytest exit 0 | green |
| TASK-W0-04 | REQ-01..14, REQ-34 | `tests/verify/*`; fixture packs under `tests/fixtures/` | co-ship live module + fixtures with `prayog:covers` | Created `tests/verify/verify_wave0_seat_bulletin.py` (covers CAP-01/CAP-02/J-*) + fixture packs; **did not** run live smoke or claim look-at success; check+pytest exit 0 | green |

## Live verify (human — not claimed here)

- Planned script: `poetry run python -m tests.verify.verify_wave0_seat_bulletin` under `tests/verify/`
- Prove rungs: CAP-01, CAP-02 / J-01, J-05, J-07, J-08, J-11, J-17
- Fixtures: `tests/fixtures/cap-01-bulletin/`, `tests/fixtures/cap-02-seat/`, `tests/fixtures/j-01-guest-feed/`, `tests/fixtures/j-05-register-login/`
- Look-ats: API JSON feed order + fail-closed status after bearer omit (human completes; ack = `wave-accepted`)
- Agent created planned FILE + fixtures: **yes** — **did not** run smoke/sandbox or claim look-at success

## Observed commands (host)

```text
make check
# → All done! 98 files would be left unchanged. (exit 0)

# Unit (host env: DATABASE_URL=postgresql://adh:adh@localhost:5432/realworld,
# SECRET_KEY=secret, APP_ENV=test; DeprecationWarning override for Py3.11 crypt;
# ROS PYTHONPATH cleared)
pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/ \
  -o 'filterwarnings=ignore::DeprecationWarning' \
  -o 'addopts=--strict-markers --tb=line --asyncio-mode=auto'
# → 95 passed in ~31s (exit 0)
```

## Forge readiness

- After this hop: `commit_workspace` (code on bound `head_ref`) — **required** by pin; skill did **not** commit/push
- Next external-action: `open_draft_pr` / `wave-pr-action`
  - title: `[INIT-REALWORLD-001 W0] Seat + public bulletin + feed order + prove scaffold`
  - body_path: `docs/specification/reports/Wave-PR-Body-INIT-REALWORLD-001-W0-realworld-api.md`
  - head_ref: `feature/init-realworld-001-w0-realworld-api`
  - base_ref: `develop`

## Notes

- Unseated mutate without Authorization returns **403** on this chassis (`RWAPIKeyHeader` / FastAPI APIKeyHeader), not 401. Product fail-closed satisfied; live expected statuses accept `[401, 403]`.
- Feed ORDER BY implemented in `ArticlesRepository.filter_articles`; DB trigger `update_article_modtime` advances `updated_at` on row update in real request transactions.

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
    wave_issue: "https://github.com/drivestream-lab/realworld-api/issues/8"
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
    test_command: "poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/"
    verify_command: "poetry run python -m tests.verify.verify_wave0_seat_bulletin"
    covers:
      - CAP-01
      - CAP-02
      - J-01
      - J-05
      - J-07
      - J-08
      - J-11
      - J-17
    fixtures:
      - tests/fixtures/cap-01-bulletin/stimulus.json
      - tests/fixtures/cap-02-seat/stimulus.json
      - tests/fixtures/j-01-guest-feed/stimulus.json
      - tests/fixtures/j-05-register-login/stimulus.json
    human_observations:
      - "API JSON feed order + fail-closed status after bearer omit"
    head_ref: feature/init-realworld-001-w0-realworld-api
    base_ref: develop
    commit_workspace: required
  next_candidates:
    - wave-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels: []
    remove_labels: []
    title: "[INIT-REALWORLD-001 W0] Seat + public bulletin + feed order + prove scaffold"
    body_path: docs/specification/reports/Wave-PR-Body-INIT-REALWORLD-001-W0-realworld-api.md
    head_ref: feature/init-realworld-001-w0-realworld-api
    base_ref: develop
```
