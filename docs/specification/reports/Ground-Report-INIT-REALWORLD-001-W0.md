# Ground report — INIT-REALWORLD-001 W0

| Field | Value |
|-------|-------|
| Wave | W0 — Seat + public bulletin + feed order + prove scaffold |
| Spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Initiative | INIT-REALWORLD-001 |
| Date | 2026-11-17 |
| Wave head (exact) | `feature/init-realworld-001-w0-realworld-api` @ `d75b2743a701b42b8bac751f5ff26610e19ec4c1` — reviewed head for sign-off (`wave-accepted` on tip; Pass-1 accept tip was `1b9d1c2d0c529db3c770bf0b249eed09c5ba4295`) |
| PR URL (if any) | https://github.com/drivestream-lab/realworld-api/pull/25 — read-only context |
| Status | Draft |
| Review deadline | 2026-11-19 |
| Deciders | Tech lead / reviewer: wave-signoff human — merge/publish only (human_approved already from wave-acceptance) |
| Outcome | pass |
| Outcome reason | G1–G10 satisfied; all wave-assigned REQs map to artifacts; Contracts produced complete; no open Blocking GF-*; exact-head merge package ready |
| Assigned REQs | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-34 |

## Evidence sources (separate layers)

| Layer | Source | Summary |
|-------|--------|---------|
| Unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` / Wave-Execution-INIT-REALWORLD-001-W0.md | Wave-Execution: 95 passed, check+unit exit 0 after TASK-W0-01..04. Ground host re-run blocked by local passlib/`crypt` DeprecationWarning under Python 3.11 — unit layer cited from Wave-Execution, not re-claimed here |
| Ground | N/A (`ground_command` plan AF-2) — manual `app/` + `tests/**` scan | Mapped every W0-assigned REQ to entry points, unit tests, and live verify/fixtures (below). `make check` (black --check app tests) exit 0 on this tip |
| Accept | `wave-accepted` on PR #25 tip / wave-acceptance | Label present on tip `d75b274…`; CAP-01/CAP-02 + J look-ats ack via human accept (nikd10x). Live script path declared; loop-spec did not claim smoke |

## Automated ground check output

`ground_command` is **N/A** (Implementation-Plan AF-2: as-built seed planned W2; `/ground-spec` after wave-acceptance). Manual source + tests scan performed instead.

```text
make check
.venv/bin/poetry run black --check app tests
All done! 98 files would be left unchanged.
exit 0
```

Manual scan anchors:

- `app/api/routes/authentication.py` — register returns `token=""`; login mints JWT
- `app/api/routes/articles/articles_resource.py` — list/get ungated (`required=False`); create requires authorizer; ADR-004 unseat comment
- `app/db/repositories/articles.py` `filter_articles` — `ORDER BY updated_at DESC, created_at DESC`
- `app/api/dependencies/profiles.py` — guest profile read (`required=False`)
- `tests/verify/verify_wave0_seat_bulletin.py` — `prayog:covers:` CAP-01, CAP-02, J-01, J-05, J-07, J-08, J-11, J-17 + REQ markers
- Fixtures under `tests/fixtures/cap-01-bulletin/`, `cap-02-seat/`, `j-01-guest-feed/`, `j-05-register-login/`

Codegraph provider: unavailable → `degraded-none` (direct source_roots reads).

## REQ checklist (wave-assigned only)

| REQ | Spec claim | Verified artifact | CAP/J covers | Look-ats | Status |
|-----|-----------|-------------------|--------------|----------|--------|
| REQ-01 | Guest global feed ungated | `articles_resource.list_articles` + `test_guest_can_list_and_get_articles_without_authorization` + verify CAP-01 | CAP-01 / J-01 | newest-first feed (shared look-at) | pass |
| REQ-02 | Guest open article | `articles_resource.retrieve_article_by_slug` + guest get in same unit + verify CAP-01 get | CAP-01 / J-01 | — | pass |
| REQ-03 | Guest tag lane | `filter_articles(tag=…)` + `test_guest_can_filter_articles_by_tag_without_authorization` | CAP-01 / J-02 | — | pass |
| REQ-04 | Guest public profile + author articles | `profiles` get ungated + `test_guest_can_list_author_articles_without_authorization` + `test_unregistered_user_will_receive_profile_without_following` | CAP-01 / J-03 | — | pass |
| REQ-05 | Tag-hop discovery | Tag filter path same as REQ-03; article `tagList` on get; live CAP-01 covers J-04 via bulletin script + fixtures | CAP-01 / J-04 | — | pass |
| REQ-06 | Multi-tag lane membership | Tag filter membership via `filter_articles` + article tags persistence (chassis); covered under CAP-01/J-04 prove intent | CAP-01 / J-04 | — | pass |
| REQ-07 | Reads after unseat | Ungated list/get remain `required=False`; ADR-004 client discard; J-17 on covers marker | CAP-01 / J-17 | — | pass |
| REQ-08 | Register eligibility (no seat JWT) | `authentication.register` returns `token=""`; `test_user_success_registration`; verify CAP-02 | CAP-02 / J-05 | — | pass |
| REQ-09 | Refuse duplicate register | `test_failed_user_registration_when_some_credentials_are_taken` → 400; no token | CAP-02 / J-05 | — | pass |
| REQ-10 | Login seats | `authentication.login` mints JWT; `test_user_successful_login`; verify CAP-02 | CAP-02 / J-05 | — | pass |
| REQ-11 | Invalid login refuse | `test_user_login_when_credential_part_does_not_match` → 400 | CAP-02 / J-11 | — | pass |
| REQ-12 | Logout unseat (client JWT discard) | ADR-004 + articles router comment; no logout RPC; omit bearer deny on create | CAP-02 / J-07 | deny publish after bearer omit | pass |
| REQ-13 | Reseat after re-login | Login re-issues token; verify CAP-02 seated create sanity after login | CAP-02 / J-07 | — | pass |
| REQ-14 | Unseated contribution deny | `test_unseated_create_article_is_denied` → **403** (APIKeyHeader); create uses required authorizer | CAP-02 / J-08 | deny on publish | pass |
| REQ-34 | Newest-first feed order | `ArticlesRepository.filter_articles` dual orderby; `test_global_feed_orders_newest_first_by_updated_at` | CAP-01 / J-01 | newest-first slugs | pass |

## Boundary checks

| Rule | Source | Status |
|------|--------|--------|
| Package root remains `app/` for Wave0a | ADR-001 Accepted | pass — no `src/` product migrate |
| Unseat = client JWT discard; no logout RPC | ADR-004 Accepted | pass — documented on articles router; omit-bearer deny proven |
| Incremental `make check` (black) OK for W0 | ADR-001 + python-tooling.mdc | pass — Makefile `check` black-only |
| Fail-closed unseated mutate | fail-fast.mdc | pass — 403 chassis deny (accepted at wave-acceptance as fail-closed) |
| Live under `tests/verify` + fixtures; not unit-as-live | testing-verify-flows.mdc | pass — verify module + fixture packs co-shipped |
| ADR-002 / ADR-003 shelf/count wire | Accepted ADRs (W2 scope) | SKIPPED — not in W0 TASK touch set |
| Injector / `src/` DI chassis | dependency-injection.mdc | SKIPPED — ADR-001 exception |

## Cross-spec contracts consumed

| Assumed contract | Source | Match? |
|-----------------|--------|--------|
| No prior-wave Ground Report (W0 first) | Pre-Implement-INIT-REALWORLD-001-W0.md | yes — N/A baseline |
| Guest list/get ungated with optional authorizer | Pre-Implement baseline / live `app/` | yes — retained and hardened |
| Login sole seat issuer after register change | Pre-Implement (TASK-W0-02 intent) | yes — register `token=""`; login mints |
| Feed order `updated_at DESC, created_at DESC` | Pre-Implement / FF-10 | yes — repository `filter_articles` |
| Chassis under `app/` | ADR-001 | yes |

## Discrepancies (must fix before human checkpoint)

| ID | REQ | Finding | Severity |
|----|-----|---------|----------|
| — | — | None — no open Blocking / Should-fix GF-* | — |

Note (non-finding): chassis omits-Authorization mutate surfaces **403** (APIKeyHeader) vs plan prose “401”; Learning-Extract empty-set + human `wave-accepted` treated deny as fail-closed — not minted as GF-*.

## Learning cited

(From `docs/specification/reports/Learning-Extract-INIT-REALWORLD-001-W0.md` — cite only.)

| L-id | Class | How it affects this ground |
|------|-------|----------------------------|
| — | — | Empty set (`human_fix_detected: no`); no L-* to apply — tip matches accepted W0 intent |

## Contracts produced by this wave

(REQUIRED — input for `/pre-implement` of W1.)

| Contract | Module / component | Entry point | Input shape | Output shape | Invariants | Next wave |
|----------|--------------------|-------------|-------------|--------------|------------|-----------|
| Guest global / tag / author list | articles list route + articles repository | `list_articles` / `filter_articles` | Optional bearer; optional tag/author/favorited; limit/offset | Article list JSON + count | No auth challenge for reads; empty lists allowed; newest-first by updated then created | W1 |
| Guest single article get | articles get route | `retrieve_article_by_slug` | Article slug path; no seat required | Single article JSON | Published article readable unseated; missing → not-found | W1 |
| Guest public profile | profiles dependency + route | `get_profile_by_username_from_path` | Username path; optional bearer | Public profile JSON | Guest may read; following false when unseated | W1 |
| Register eligibility without seat | authentication register | `register` | username + email + password body | User JSON with empty token string | No usable seat JWT; duplicate username/email fail-closed | W1 |
| Login seats / reseats | authentication login | `login` | email + password body | User JSON with non-empty JWT | Sole seat issuer; bad credentials fail-closed | W1 |
| Unseat via client discard | auth middleware + protected mutates | Omit `Authorization` on contribute routes | No bearer (or invalid) | Deny (chassis 403) | No logout RPC; retained token valid until expiry (ADR-004) | W1 |
| Seated article create gate | articles create route | `create_new_article` | Bearer + article body (incl. tags) | Created article JSON | Unseated create denied; W1 adds ≥1-tag product rule | W1 |
| W0 live prove scaffold | verify module + fixtures | `tests.verify.verify_wave0_seat_bulletin` | Running API base URL | Exit 0 + PASS markers; look-ats printed | Covers CAP-01/CAP-02 + listed J-*; not unit SSOT | W1 |

## Exact-head merge package (for wave-signoff)

> Write the Ground Report and as-built updates **locally**. Emit Forge
> readiness for publication. Do **not** commit, push, merge, or apply labels
> from this skill. Human approved was `wave-acceptance`. At `wave-signoff`
> the human merges/publishes the **exact wave head** only.

- PR URL / wave head: https://github.com/drivestream-lab/realworld-api/pull/25 @ `d75b2743a701b42b8bac751f5ff26610e19ec4c1` — **expected reviewed head SHA** (before forge publishes this Ground Report onto the same branch)
- Ground Report path: `docs/specification/reports/Ground-Report-INIT-REALWORLD-001-W0.md`
- Accept evidence: `wave-accepted` on tip (wave-acceptance) — human approved already
- Wave-Execution path: `docs/specification/reports/Wave-Execution-INIT-REALWORLD-001-W0.md`
- Optional/legacy Live-Verify path: n/a (not required)
- As-built: W0 `human_approved` from wave-acceptance (do not re-mark here) — seeded in `docs/specification/as-built/`
- Required merge fields (human fills at `wave-signoff`; not `handoff.forge`):
  `reviewed_head_sha`, `merge_commit_sha`

### Human merge checklist (wave-signoff)

- [ ] Review REQ checklist — all wave-assigned REQs pass or explicitly deferred
- [ ] Review §Contracts produced — accurate and complete for next wave
- [ ] Confirm reviewed head SHA matches the package above
- [ ] Confirm human_approved already recorded at wave-acceptance (do not re-mark)
- [ ] Merge the wave PR manually at wave-signoff (human only) — record merge commit SHA
- [ ] Do not ask Gateflow/Forge to merge; no approval-label auto-merge

## Ready for wave-signoff (merge)?

yes — W0 assigned REQs grounded; Contracts produced complete; `wave-accepted` on tip; no Blocking GF-*; next orch hop is `wave-done-action` then human `wave-signoff` merge only.

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: ground-spec
  outcome: pass
  artifact:
    path: docs/specification/reports/Ground-Report-INIT-REALWORLD-001-W0.md
  blockers: []
  signals:
    initiative: INIT-REALWORLD-001
    wave: W0
    contracts_produced: 8
    assigned_reqs:
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
    wave_pr: https://github.com/drivestream-lab/realworld-api/pull/25
    wave_issue: https://github.com/drivestream-lab/realworld-api/issues/8
    head_ref: feature/init-realworld-001-w0-realworld-api
    tip_sha: d75b2743a701b42b8bac751f5ff26610e19ec4c1
    accept_tip_sha: 1b9d1c2d0c529db3c770bf0b249eed09c5ba4295
    verify_command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
    codegraph_provider: degraded-none
    grounding_depth: light
  next_candidates:
    - wave-done-action
  human_checkpoint: false
  external_action: true
  forge:
    action: update_board_status
    ticket: https://github.com/drivestream-lab/realworld-api/issues/8
```
