## Pre-implement — realworld-api / W0 — Seat + public bulletin + feed order + prove scaffold

| Field | Value |
|-------|-------|
| Artifact | `docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md` |
| Initiative | INIT-REALWORLD-001 |
| Wave | W0 |
| Date | 2026-11-17 |
| Outcome | `pass` |
| Outcome reason | Spec merged with `spec-lgtm`, board EPIC/waves seeded with TASK projection, WorkManifest contract pass, PE sign-off complete, commands resolved, wave head bound |
| Wave head context | Bound by Forge/human context: `feature/init-realworld-001-w0-realworld-api` (cut from integration `develop`) — not opened by this skill |

---

### Gate check (prior wave)

> Complete this before reading anything else. Do not proceed if the gate fails.
> Board / branch / PR checks are **read-only**. Do not create tickets or open
> a branch from this skill — emit Forge readiness instead.

| Item | Required | Status |
|------|----------|--------|
| Branch context (read-only) | Bound head is `develop` or `feature/INIT-*-w{N}-*` — not open `chore/*-spec-*` | [x] ok — Lead-bound `feature/init-realworld-001-w0-realworld-api` from `develop` (local checkout currently on `develop`; skill does not open/create branch) |
| Spec PR merged | Implementation plan on integration branch | [x] yes — PR #3 merge commit `8e6d19ba7efef485a6ac86719092e7f292f156bc` on `develop`; plan at `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md` |
| Coding-readiness at merge | Merged spec PR had `spec-lgtm` on head | [x] verified — PR #3 labels include `spec-lgtm`; APPROVED reviews on head `266c56b405646c28b1ffc1144e1a9e7800304c2b` |
| Board seed (read-only) | Wave issue(s) from plan §9 exist; TASK ids present in wave body | [x] seeded — EPIC #7; waves #8 (W0), #9 (W1), #10 (W2); W0/W1/W2 are sub-issues of #7; W0 body lists TASK-W0-01..04 |
| WorkManifest contract | `prayog/v1` §9 passes `scripts/workmanifest_contract.py` | [x] pass — `PYTHONPATH=prayog-skills:. python3 prayog-skills/scripts/workmanifest_contract.py docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md --base-path .` exit 0 |
| TASK exit proof | Every wave `TASK-*` has `exit.criteria` + `exit.proof` (kind/expected/evidence_expected) | [x] complete — TASK-W0-01..04 |
| Live-verification contract | When P15 applies: `verification.live` applicable + script under `live_verify_dir` + fixtures under `fixtures_dir`; `covers` include `CAP-*` and/or `J-*`; deps/preflight; look-ats when opaque | [x] contract — live applicable; command `poetry run python -m tests.verify.verify_wave0_seat_bulletin`; covers CAP/J; fixtures + `human_observations` declared (FILEs co-ship in `/loop-spec`) |
| Prove rungs (`CAP-*` / `J-*`) | Listed ids match plan/manifest live covers | [x] listed — CAP-01, CAP-02 / J-01, J-05, J-07, J-08, J-11, J-17 |
| Fixture packs | Paths under `fixtures_dir` present in FILE list / `fixtures[]` | [x] path — `tests/fixtures/cap-01-bulletin/`, `tests/fixtures/cap-02-seat/`, `tests/fixtures/j-01-guest-feed/`, `tests/fixtures/j-05-register-login/` (create in TASK-W0-04) |
| Human look-ats | `human_observations` when opaque; else N/A | [x] listed — API JSON feed order + 401 after bearer omit |
| Plan source freshness | all upstream rows `CURRENT` | [x] current — product-spec H1/H2/H3 match live PRD + Impact-Map rev 1; plan table CURRENT |
| Impact-map repo scope | revision and scope digest match canonical handoff | [x] match — H3=`1`; H2=`sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d` |
| `check_command` | resolved | [x] `make check` |
| `test_command` | resolved | [x] `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` |
| `verify_command` | live script under `live_verify_dir` when P15 applies; else command or N/A with reason | [x] `poetry run python -m tests.verify.verify_wave0_seat_bulletin` |
| `ground_command` | resolved or N/A with reason | [x] N/A — as-built seeded in W2; `/ground-spec` after wave-acceptance (plan AF-2) |
| Co-shipped live verify (P15) | If wave adds/changes product surface: FILE under `live_verify_dir` + pack under `fixtures_dir`; covers CAP/J | [x] path — `tests/verify/verify_wave0_seat_bulletin.py` + fixture packs (co-ship TASK-W0-04) |
| Prior wave as-built row | `human_approved` (from prior `wave-acceptance`) | [x] N/A — W0 first wave (no prior as-built row) |
| Prior Ground Report exists | `reports/Ground-Report-{SPEC}-W{N-1}.md` | [x] N/A — W0 (no prior Ground Report) |
| Plan PE sign-off (W0 only) | Implementation-Plan §0 marked complete | [x] complete — 2026-11-11 |

**Gate verdict:** PASS — W0 PE sign-off complete; spec merge + `spec-lgtm` + board seed + WorkManifest + command/live contracts satisfied.

**Forge readiness (when seed / wave head absent):** not required for seed (present). Wave head is Lead-bound — publish checklist via `commit_workspace` onto `feature/init-realworld-001-w0-realworld-api` (do **not** mutate from this skill).

---

### Contracts consumed (from prior Ground Report)

> W0 has no prior Ground Report. Contracts below are **baseline as-is** from
> `source_roots` (`app/` per ADR-001), not Ground-Report–attested.

| Assumed contract | Entry point | Input shape | Output shape | Source | Confirmed? |
|-----------------|-------------|-------------|--------------|--------|------------|
| Guest list/get articles ungated | `app/api/routes/articles/articles_resource.py` `list_articles` / `get_article` | Optional bearer; filters (tag/author/favorited/limit/offset); slug path | Article list or single article JSON | live `app/` scan | [x] yes — `get_current_user_authorizer(required=False)` on list; mutate routes require authorizer |
| Register currently mints seat JWT | `app/api/routes/authentication.py` `register` | username/email/password body | User + token | live `app/` scan | [x] yes — `jwt.create_access_token_for_user` on register (TASK-W0-02 must stop minting) |
| Login seats | `app/api/routes/authentication.py` `login` | email/password body | User + token | live `app/` scan | [x] yes — token issued on valid credentials |
| Feed ordering | `app/db/queries/sql/articles.sql` list query | filter params | article rows | live SQL | [x] yes — current `ORDER BY a.created_at` (TASK-W0-03 must change to `updated_at DESC, created_at DESC`) |
| Package chassis under `app/` | modules under `app/` | N/A | N/A | ADR-001 + tree | [x] yes — no `src/` product tree for Wave0a |

**Unconfirmed contracts** (prior wave not yet grounded or source not found):
- No prior-wave Ground Report contracts — W0 is first implement wave.
- Cross-repo consumers (`realworld-web`, `realworld-local`) are out of this repo’s W0 coding scope; CTR-01/CTR-02 assumed by product but not grounded here → flag only as merge-order dependency for UAT, not a W0 coding blocker.

---

### Must read

- [x] `AGENTS.md`
- [x] MDC rules (domain-filtered — list files read for this slice's domains):
  - [x] `architecture.mdc` — layout / JWT / packages (Wave0a exception via ADR-001)
  - [x] `fail-fast.mdc` — denial / no silent fallback (seat + unseated mutate)
  - [x] `http-api-conventions.mdc` — body/query/path for auth + articles
  - [x] `repository-pattern.mdc` — repo boundary for articles ordering
  - [x] `pydantic-schemas.mdc` — existing schemas under `app/models` (retain chassis)
  - [x] `testing-verify-flows.mdc` — verify vs pytest; live under `tests/verify`
  - [x] `python-tooling.mdc` — incremental `make check` in W0
  - [x] skipped: `dependency-injection.mdc` — ADR-001 retains `app/` without injector migrate
  - [x] skipped: `infra-services.mdc` — no new infra client
  - [x] skipped: `logging-loguru.mdc` — NFR observability not a W0 kill criterion
- [x] ADRs (keyword-matched — list ids):
  - [x] ADR-001 — Wave0a package chassis under `app/` (Accepted)
  - [x] ADR-004 — unseat via client JWT discard; no logout RPC (Accepted)
  - [x] ADR-002 — private-shelf `favorited=` auth (Accepted; W2 primary; cited for initiative completeness)
  - [x] ADR-003 — `favoritesCount` wire policy (Accepted; W2 primary; cited for initiative completeness)
- [x] Spec: `docs/specification/product/INIT-REALWORLD-001-api.md`
- [x] Plan wave section / §9 WorkManifest: `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md` W0
- [x] Board wave issue: https://github.com/drivestream-lab/realworld-api/issues/8 — TASK list (projected from WorkManifest; not a second authority):
  - [x] TASK-W0-01 — implements REQ-01 — depends_on: [] — files: `Makefile` modify; `tests/README.md` create — exit proof: command/`make check` → exit 0
  - [x] TASK-W0-02 — implements REQ-08, REQ-09, REQ-10, REQ-11 — depends_on: [TASK-W0-01] — files: `app/api/routes/authentication.py`; registration/login tests — exit proof: command/pytest seat assertions
  - [x] TASK-W0-03 — implements REQ-01..07, REQ-12..14, REQ-34 — depends_on: [TASK-W0-02] — files: articles repo/SQL + articles routes + article/profile tests — exit proof: command/pytest order + 401
  - [x] TASK-W0-04 — implements REQ-01..14, REQ-34 — depends_on: [TASK-W0-03] — files: `tests/verify/verify_wave0_seat_bulletin.py` + CAP/J fixtures — exit proof: command/live verify; evidence `wave-accepted on tip`

---

### Governance alignment

- [x] Slice spec does not contradict any listed ADR (ADR-001/`app/` chassis; ADR-004 client discard unseat)
- [x] Plan TASK MDC notes and ADR notes for this wave reviewed
- [x] Every initiative ADR cited for this wave is **Accepted** in `docs/specification/adr`
  (ADR-001..004 Accepted; created during `/spec-technical-review`)

---

### Must update (in the same change as the code — via `/loop-spec`)

- [ ] Product spec — `docs/specification/product/INIT-REALWORLD-001-api.md` only if W0 coding discovers contract drift (otherwise leave; Status still says Draft prose — not authority for H1–H3)
- [ ] `as-built/implementation-status.md` — N/A for W0 seed (plan: as-built in W2); do not invent premature as-built in W0 unless loop-spec discovers a required harness pointer
- [ ] `tests/README.md` — create feature map (TASK-W0-01) pointing at live modules
- [ ] Unit verification scope — registration/login seat rules; guest reads; newest-first order; 401 without bearer (TASK-W0-02..03)
- [ ] Live verification — co-ship `tests/verify/verify_wave0_seat_bulletin.py` + fixture packs under `tests/fixtures/` covering CAP-01/CAP-02 / J-01/J-05/…; human-run + look-ats at `wave-acceptance`
- [ ] ADR — no supersede expected for W0; retain ADR-001/004

---

### Must not

- [ ] Implement against spec wording that contradicts an Accepted ADR without
  first superseding that ADR
- [ ] Duplicate unit verification assertions in live smoke scripts
- [ ] Assume a contract from a prior wave is correct without checking the
  Ground Report (or flagging it as unconfirmed above)
- [ ] Open a branch, commit, push, open a PR, apply labels, or create board
  issues from this skill
- [ ] Migrate package root to `src/` in this wave (contradicts Accepted ADR-001)
- [ ] Add logout RPC / server revoke store (contradicts Accepted ADR-004)

---

### Verification plan

| Layer | What it proves | Command (from tests_readme / profile) |
|-------|----------------|---------------------------------------|
| Static check | Formatting/lint incremental tooling for W0 | `make check` |
| Unit | Module logic, seat rules, order + 401 edges (Postgres fixtures allowed at existing test boundary) | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` |
| Live verify | CAP-01/CAP-02 and journeys on real compose infra (human-run at `wave-acceptance`) | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` + fixtures; covers CAP/J; look-ats for feed order + 401 |
| Ground check | Assigned wave REQs satisfied; boundaries respected | N/A — as-built/ground after W2 seed; Pass-2 `/ground-spec` after wave-acceptance |

> P15 applies: live verify must not be N/A or unit-only.
> Agent implements the script in `/loop-spec`; does **not** run it as success.
> Policy: live-smoke-policy.md.

### Human wave-acceptance (after loop-spec + Draft PR)

When checklist PASS and coding is green, the human at checkpoint
`wave-acceptance`:

- [ ] Run `poetry run python -m tests.verify.verify_wave0_seat_bulletin` against realworld-local compose
- [ ] Look-ats: newest-first slugs in feed JSON; 401 on publish after bearer omit
- [ ] Signal accept with GitHub label `wave-accepted` on the tip (phase-1)
- [ ] Apply tip hygiene for any hotfixes before Enter-at Pass-2 closeout
- [ ] Optional/legacy notes may land in `Live-Verify-*` — not required for the gate

---

### Tracker / PR (read-only context)

- Initiative: INIT-REALWORLD-001
- Issue: #8 (EPIC parent #7)
- Spec path: `docs/specification/product/INIT-REALWORLD-001-api.md`
- Verify command (human): `poetry run python -m tests.verify.verify_wave0_seat_bulletin`
- ADRs in scope: ADR-001, ADR-004 (primary); ADR-002, ADR-003 (initiative Accepted set)
- Wave head: bound by Forge/human context — `feature/init-realworld-001-w0-realworld-api`

---

### Checklist publish readiness (on `pass` — fill handoff.forge commit_workspace)

| Field | Value |
|-------|-------|
| Workflow outcome | `pass` — W0 preflight gates satisfied |
| Next | `loop-spec` (`skill`) — `external_action: false` |
| Forge (this hop) | `commit_workspace` **required** — publish `docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md` to bound `head_ref` |
| Later | After `/loop-spec`, `wave-pr-action` opens Draft PR (checklist + code already on tip) |

Recommend `/commit-workspace` after explicit authorization. Do not open the PR here.

---

### Merge order (if cross-module / cross-service)

N/A for coding this wave inside `realworld-api` alone. UAT prove later depends on `realworld-api` → `realworld-web` → `realworld-local` (Impact-Map §7) but is not a W0 serial TASK dependency inside this repo.

---

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: pre-implement
  outcome: pass
  artifact:
    path: docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md
  blockers: []
  signals:
    initiative: INIT-REALWORLD-001
    wave: W0
    board_epic: https://github.com/drivestream-lab/realworld-api/issues/7
    board_wave_issue: https://github.com/drivestream-lab/realworld-api/issues/8
    tasks:
      - TASK-W0-01
      - TASK-W0-02
      - TASK-W0-03
      - TASK-W0-04
    workmanifest_contract: pass
    check_command: make check
    test_command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
    verify_command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
    ground_command: null
    ground_command_reason: N/A — as-built seeded in W2; /ground-spec after wave-acceptance
    head_ref: feature/init-realworld-001-w0-realworld-api
    integration_branch: develop
    spec_pr: https://github.com/drivestream-lab/realworld-api/pull/3
    spec_lgtm: true
    pe_signoff: complete
    codegraph_provider: degraded-none
    grounding_depth: none
  next_candidates:
    - loop-spec
  human_checkpoint: false
  external_action: false
  forge:
    action: commit_workspace
    head_ref: feature/init-realworld-001-w0-realworld-api
    paths:
      - docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md
```
