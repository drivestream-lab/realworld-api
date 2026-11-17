## Pre-implement — realworld-api / W0 — Seat + public bulletin + feed order + prove scaffold

| Field | Value |
|-------|-------|
| Artifact | `docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md` |
| Initiative | INIT-REALWORLD-001 |
| Wave | W0 |
| Date | 2026-11-17 |
| Outcome | `pass` |
| Outcome reason | Spec merged with `spec-lgtm`, board EPIC/waves seeded with TASK projection, WorkManifest + live contract clean, PE sign-off complete, wave head bound |
| Wave head context | Bound by Forge/human context: `feature/init-realworld-001-w0-realworld-api` (cut from `develop`) — not opened by this skill |

---

### Gate check (prior wave)

> Complete this before reading anything else. Do not proceed if the gate fails.
> Board / branch / PR checks are **read-only**. Do not create tickets or open
> a branch from this skill — emit Forge readiness instead.

| Item | Required | Status |
|------|----------|--------|
| Branch context (read-only) | Bound head is `develop` or `feature/INIT-*-w{N}-*` — not open `chore/*-spec-*` | [x] ok — `feature/init-realworld-001-w0-realworld-api` (Lead/Forge bind; integration base `develop`) |
| Spec PR merged | Implementation plan on integration branch | [x] yes — PR [#3](https://github.com/drivestream-lab/realworld-api/pull/3) merged to `develop` (`mergeCommit` `8e6d19ba7efef485a6ac86719092e7f292f156bc`) |
| Coding-readiness at merge | Merged spec PR had `spec-lgtm` on head | [x] verified — label `spec-lgtm` present on merged PR #3 |
| Board seed (read-only) | Wave issue(s) from plan §9 exist; TASK ids present in wave body | [x] seeded — EPIC [#7](https://github.com/drivestream-lab/realworld-api/issues/7); W0 [#8](https://github.com/drivestream-lab/realworld-api/issues/8); W1 [#9](https://github.com/drivestream-lab/realworld-api/issues/9); W2 [#10](https://github.com/drivestream-lab/realworld-api/issues/10); W0–W2 are sub-issues of EPIC #7 |
| WorkManifest contract | `prayog/v1` §9 passes `scripts/workmanifest_contract.py` | [x] pass — `WorkManifest contract passed.` |
| TASK exit proof | Every wave `TASK-*` has `exit.criteria` + `exit.proof` (kind/expected/evidence_expected) | [x] complete — TASK-W0-01..04 |
| Live-verification contract | When P15 applies: `verification.live` applicable + script under `live_verify_dir` + fixtures under `fixtures_dir`; `covers` include `CAP-*` and/or `J-*`; deps/preflight; look-ats when opaque | [x] contract — `poetry run python -m tests.verify.verify_wave0_seat_bulletin`; fixtures under `tests/fixtures/` |
| Prove rungs (`CAP-*` / `J-*`) | Listed ids match plan/manifest live covers | [x] listed — CAP-01, CAP-02 / J-01, J-05, J-07, J-08, J-11, J-17 |
| Fixture packs | Paths under `fixtures_dir` present in FILE list / `fixtures[]` | [x] path — `tests/fixtures/cap-01-bulletin/`, `cap-02-seat/`, `j-01-guest-feed/`, `j-05-register-login/` (co-ship in TASK-W0-04) |
| Human look-ats | `human_observations` when opaque; else N/A | [x] listed — API JSON feed order + 401 after bearer omit |
| Plan source freshness | product-spec H1–H3 (+ G1) match live durable roots | [x] current — H1 `sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4`; H2 `sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d`; H3 `1`; G1 meta head `a500df8eeefbea095ecdd65e00edb128416c3cf4` |
| Impact-map repo scope | revision and scope digest match canonical handoff | [x] match — Impact-Map rev 1; realworld-api scope digest matches product-spec H2 |
| `check_command` | resolved | [x] `make check` |
| `test_command` | resolved | [x] `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` |
| `verify_command` | live script under `live_verify_dir` when P15 applies; else command or N/A with reason | [x] `poetry run python -m tests.verify.verify_wave0_seat_bulletin` |
| `ground_command` | resolved or N/A with reason | [x] N/A — as-built seeded in W2; `/ground-spec` after wave-acceptance (plan AF-2) |
| Co-shipped live verify (P15) | If wave adds/changes product surface: FILE under `live_verify_dir` + pack under `fixtures_dir`; covers CAP/J | [x] path — `tests/verify/verify_wave0_seat_bulletin.py` + fixture packs (TASK-W0-04) |
| Prior wave as-built row | `human_approved` (from prior `wave-acceptance`) | [x] N/A — W0 first wave |
| Prior Ground Report exists | `reports/Ground-Report-{SPEC}-W{N-1}.md` | [x] N/A — W0 first wave |
| Plan PE sign-off (W0 only) | Implementation-Plan §0 marked complete | [x] complete — 2026-11-11 |

**Gate verdict:** PASS — W0 PE sign-off complete; spec merge + `spec-lgtm` + board seed + WorkManifest/live contracts satisfied; wave head bound.

**Forge readiness (when seed / wave head absent):** N/A — seed present; head bound. On pass, publish this checklist via `commit_workspace` (see handoff).

---

### Contracts consumed (from prior Ground Report)

> W0 has no prior Ground Report. Baseline interfaces confirmed by scanning
> `app/` (ADR-001 package root) — not assumed from spec alone.

| Assumed contract | Entry point | Input shape | Output shape | Source | Confirmed? |
|-----------------|-------------|-------------|--------------|--------|------------|
| Register currently mints a seat token (TASK-W0-02 must stop this) | `app/api/routes/authentication.py` → `register` | username + email + password body | membership + token field present | live source scan | [x] yes — token minted today |
| Login seats via JWT | `app/api/routes/authentication.py` → `login` | email + password body | user + access token | live source scan | [x] yes |
| Guest global list is ungated | `app/api/routes/articles/articles_resource.py` → `list_articles` | optional filters; optional user | article list | live source scan | [x] yes — `get_current_user_authorizer(required=False)` |
| Global feed ordering not newest-first by update time (TASK-W0-03) | `ArticlesRepository.filter_articles` (`app/db/repositories/articles.py`) | tag/author/favorited + limit/offset | unordered / insertion-order list (no `ORDER BY updated_at DESC, created_at DESC`) | live source scan | [x] yes — no ORDER BY on filter path; feed SQL uses `ORDER BY a.created_at` only |

**Unconfirmed contracts** (prior wave not yet grounded or source not found):
- None for W0 — no prior-wave Ground Report dependency. Cross-repo prove env (`realworld-local` compose) is a runtime dependency for live verify, not a code contract from a prior wave.

---

### Must read

- [x] `AGENTS.md`
- [x] MDC rules (domain-filtered — list files read for this slice's domains):
  - [x] `architecture.mdc` — layout / JWT; Wave0a exception via ADR-001 (`app/` retained)
  - [x] `fail-fast.mdc` — denial / no silent fallback (seat + auth failures)
  - [x] `http-api-conventions.mdc` — body/query/path for auth + articles
  - [x] `repository-pattern.mdc` — repo boundary for articles ordering change
  - [x] `pydantic-schemas.mdc` — request/response schemas
  - [x] `testing-verify-flows.mdc` — live verify vs pytest
  - [x] `python-tooling.mdc` — incremental `make check` in W0
  - skipped: `dependency-injection.mdc` — ADR-001 retains `app/` without injector migrate
  - skipped: `infra-services.mdc` — no new infra client
  - skipped: `logging-loguru.mdc` — observability N/A as kill criterion
  - skipped: `database-migrations.mdc` — W0 TASK file set has no schema migration
- [x] ADRs (keyword-matched — list ids):
  - [x] ADR-001 — Wave0a package chassis under `app/` (Accepted)
  - [x] ADR-004 — unseat via client JWT discard; no logout RPC (Accepted)
  - skipped this wave: ADR-002 / ADR-003 — private shelf / favoritesCount (W2)
- [x] Spec: `docs/specification/product/INIT-REALWORLD-001-api.md`
- [x] Plan wave section / §9 WorkManifest: `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md` W0
- [x] Board wave issue: https://github.com/drivestream-lab/realworld-api/issues/8 — TASK list (projected from WorkManifest; not a second authority):
  - [x] TASK-W0-01 — implements REQ-01 — depends_on: [] — files: `Makefile`, `tests/README.md` — exit proof: `make check` exit 0
  - [x] TASK-W0-02 — implements REQ-08, REQ-09, REQ-10, REQ-11 — depends_on: [TASK-W0-01] — files: `app/api/routes/authentication.py`, registration/login tests — exit proof: pytest seat assertions
  - [x] TASK-W0-03 — implements REQ-01..07, REQ-12..14, REQ-34 — depends_on: [TASK-W0-02] — files: articles repo/resource + article/profile tests — exit proof: pytest order + 401
  - [x] TASK-W0-04 — implements REQ-01..14, REQ-34 — depends_on: [TASK-W0-03] — files: `tests/verify/verify_wave0_seat_bulletin.py` + CAP/J fixtures — exit proof: live verify exit 0; evidence `wave-accepted on tip`

---

### Governance alignment

- [x] Slice spec does not contradict any listed ADR (ADR-001/004 Accepted; product_constraints bind seat + bulletin REQs)
- [x] Plan TASK MDC notes and ADR notes for this wave reviewed
- [x] Every initiative ADR cited for this wave is **Accepted** in `docs/specification/adr`
  (ADR-001, ADR-004; ADR-002/003 Accepted but W2-scoped)

---

### Must update (in the same change as the code — via `/loop-spec`)

- [ ] Product spec — `docs/specification/product/INIT-REALWORLD-001-api.md` (only if wire/observable contract drifts; prefer no silent amend)
- [ ] `as-built/implementation-status.md` — N/A this wave (plan seeds as-built in W2 / TASK-W2-03)
- [ ] `tests/README.md` — create feature map (TASK-W0-01) pointing at live modules
- [ ] Unit verification scope — registration/login seat rules; guest reads; newest-first; unseated mutate 401
- [ ] Live verification — co-ship `tests/verify/verify_wave0_seat_bulletin.py` + fixture packs under `tests/fixtures/` (`CAP-01` / `CAP-02`, `J-01` / `J-05`…); human-run + look-ats at `wave-acceptance`
- [ ] ADR — update only if this wave supersedes Accepted ADR-001/004 (requires PE review) — not expected

---

### Must not

- [ ] Implement against spec wording that contradicts an Accepted ADR without
  first superseding that ADR
- [ ] Duplicate unit verification assertions in live smoke scripts
- [ ] Assume a contract from a prior wave is correct without checking the
  Ground Report (or flagging it as unconfirmed above)
- [ ] Open a branch, commit, push, open a PR, apply labels, or create board
  issues from this skill
- [ ] Relocate package root to `src/` in W0 (contradicts ADR-001)
- [ ] Add a logout RPC / server revoke store (contradicts ADR-004)

---

### Verification plan

| Layer | What it proves | Command (from tests_readme / profile) |
|-------|----------------|---------------------------------------|
| Static check | Formatting / lint gate after Makefile `check` lands | `make check` |
| Unit | Seat lifecycle + guest bulletin + order + 401 edges (Postgres via existing async fixtures) | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` |
| Live verify | CAP-01/CAP-02 (+ J-01, J-05, J-07, J-08, J-11, J-17) on real local-compose infra | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` + fixtures; look-ats: newest-first slugs; 401 on publish after bearer omit |
| Ground check | Assigned wave REQs satisfied; boundaries respected | N/A — as-built seeded in W2; `/ground-spec` after wave-acceptance |

> P15 applies: live verify is required. Agent implements the script in `/loop-spec`; does **not** run it as success.
> Policy: live-smoke-policy.md.

### Human wave-acceptance (after loop-spec + Draft PR)

When checklist PASS and coding is green, the human at checkpoint
`wave-acceptance`:

- [ ] Run `poetry run python -m tests.verify.verify_wave0_seat_bulletin` against realworld-local compose
- [ ] Inspect API JSON for feed order + 401 after bearer omit
- [ ] Signal accept with GitHub label `wave-accepted` on the tip
- [ ] Apply tip hygiene for any hotfixes before Enter-at Pass-2 closeout
- [ ] Optional/legacy notes may land in `Live-Verify-*` — not required for the gate

---

### Tracker / PR (read-only context)

- Initiative: INIT-REALWORLD-001
- Issue: [#8](https://github.com/drivestream-lab/realworld-api/issues/8) (EPIC [#7](https://github.com/drivestream-lab/realworld-api/issues/7))
- Spec path: `docs/specification/product/INIT-REALWORLD-001-api.md`
- Verify command (human): `poetry run python -m tests.verify.verify_wave0_seat_bulletin`
- ADRs in scope: ADR-001, ADR-004 (W0); ADR-002, ADR-003 deferred to W2
- Wave head: bound by Forge/human context — `feature/init-realworld-001-w0-realworld-api`

---

### Checklist publish readiness (on `pass` — fill handoff.forge commit_workspace)

| Field | Value |
|-------|-------|
| Workflow outcome | `pass` — W0 preflight clean |
| Next | `loop-spec` (`skill`) — `external_action: false` |
| Forge (this hop) | `commit_workspace` **required** — publish `docs/specification/reports/Pre-Implement-INIT-REALWORLD-001-W0.md` to bound `head_ref` |
| Later | After `/loop-spec`, `wave-pr-action` opens Draft PR (checklist + code already on tip) |

Recommend `/commit-workspace` after explicit authorization. Do not open the PR here.

---

### Merge order (if cross-module / cross-service)

N/A for coding order inside realworld-api W0. Live prove depends on `realworld-local` compose (api reachable) at `wave-acceptance` — not a merge blocker for this checklist.

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
    board_epic: "https://github.com/drivestream-lab/realworld-api/issues/7"
    board_issue: "https://github.com/drivestream-lab/realworld-api/issues/8"
    tasks:
      - TASK-W0-01
      - TASK-W0-02
      - TASK-W0-03
      - TASK-W0-04
    check_command: make check
    test_command: "poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/"
    verify_command: "poetry run python -m tests.verify.verify_wave0_seat_bulletin"
    ground_command: "N/A — as-built seeded in W2"
    head_ref: feature/init-realworld-001-w0-realworld-api
    base_ref: develop
    spec_pr: "https://github.com/drivestream-lab/realworld-api/pull/3"
    spec_lgtm: true
    workmanifest_contract: pass
    pe_signoff: complete
    codegraph_provider: degraded-none
    grounding_depth: light
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
