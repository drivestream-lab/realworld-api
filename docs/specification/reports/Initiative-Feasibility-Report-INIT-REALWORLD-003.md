# Feasibility report — INIT-REALWORLD-003

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-003 |
| Spec | `docs/specification/product/INIT-REALWORLD-003-api.md` |
| PRD digest | `sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-003.md` / `1` |
| Repo scope digest | `sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7` |
| Approved meta PR head | `abfbbcff877a83c298776fd4801b8ac4c75ddfba` |
| Impact-map approval | Review `PRR_kwDOVac9Rs8AAAABXCDSZQ` / id `5840622181` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T10:48:57Z`; `commit_id` = `abfbbcff877a83c298776fd4801b8ac4c75ddfba` (meta PR [#10](https://github.com/drivestream-lab/realworld-meta/pull/10) MERGED; label `impact-map-lgtm`) |
| Source freshness | CURRENT — H1 live PRD digest matches spec citation; H2 api scope digest recomputed match (`capabilities=CAP-01,CAP-02,CAP-03`); H3 `map_revision=1`; G1 APPROVED review `commit_id` equals merged meta PR #10 head; ripple `continue` |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Branch | `chore/INIT-REALWORLD-003-spec-realworld-api` — proposed Draft spec PR (none open yet; Gate 2 stays `spec-pending`) |
| Initiative segment | `INIT-REALWORLD-003` |
| Status | Draft |
| Review deadline | 2026-11-17 |
| Deciders | PM: programme PM · Domain SME: @drivestream-lab/backend-devs |

## Summary

INIT-REALWORLD-003 is **buildable** on the Accepted Wave0a Conduit baseline under `app/`: CAP-01..CAP-03 are a **greenfield** private park/recall/relabel/discard surface (no saved-search tables or routes today), while seat gating and durable membership retention reuse existing JWT seat + Postgres patterns (ADR-001 / ADR-004). Source freshness is **CURRENT**. Zero unresolved blocking PM/PE/ADR findings — IM defaults are already locked into REQ-01..REQ-16; chassis Q-08 resolves to continue Accepted ADR-001. Proceed to `/spec-technical-review` (outcome `pass`); do not set `spec-lgtm`.

**Findings:** 4 total (0 Critical, 0 Should fix, 4 Verify / Gap)

### Derived counts (lane × severity)

| Lane | Blocking open | Non-blocking open | Resolved |
|------|---------------|-------------------|----------|
| PM | 0 | 0 | 7 (Q-01..Q-07 / IM-01..IM-07 defaults) |
| PE / ADR | 0 | 0 | 1 (Q-08 chassis → cite Accepted ADR-001 continue `app/`) |
| Domain | 0 | 0 | 0 |
| Auto-fix | 0 | 4 | 0 |

| Severity | Unresolved count |
|----------|------------------|
| Critical | 0 |
| Should fix | 0 |
| Verify / Gap (informational) | 4 |

### Selected workflow outcome

| Field | Value |
|-------|-------|
| Outcome | `pass` |
| Rationale | Zero unresolved blocking findings; informational Verify/Gap (harness, as-built, greenfield gaps, Q-08 cite ADR-001) may remain |
| Next (from workflow) | `spec-technical-review` |

Informational observations alone do **not** select `findings`. Unresolved
blocking PE/ADR → `findings`; blocking PM/domain → `needs-input`.

## Baseline snapshot (F1)

| Area | Current state | Evidence |
|------|---------------|----------|
| Unit / in-process tests | Present under `tests/test_api/`, `tests/test_services/`, `tests/test_schemas/`, `tests/test_db/` (not `tests/unit/`). Auth, users, articles/favorites, profiles/follow covered. **No** park/saved-search tests. | `tests/test_api/test_routes/test_login.py`, `test_articles.py`, `test_profiles.py`; `pyproject.toml` |
| Live verify | **Absent** as SDD `tests/verify/` + `tests/README.md`. Makefile `verify` is a single host curl to `localhost:3100/api/articles`. | `Makefile` `verify` target; no `tests/verify/`; no `tests/README.md` |
| As-built | **Absent** — `docs/specification/as-built/` empty | Spec A-07; empty `docs/specification/as-built/` |
| Source layout | Legacy Conduit package under `app/` (routes, asyncpg repos, Alembic). **No** `src/` tree. Covered by Accepted ADR-001 Option A. | `app/main.py`, `app/api/routes/api.py`; ADR-001 |
| Toolchain | Poetry; black; pytest; Makefile `verify` only (no `make check` / pyright / import-linter yet) | `pyproject.toml`, `Makefile` |
| ADRs | ADR-001..006 **Accepted** (001–004 INIT-001; 005–006 INIT-002). No INIT-003 ADRs yet — none required at feasibility. | `docs/specification/adr/adr-001-*.md` … `adr-006-*.md` (Status: Accepted) |
| Park / search-memory surface | **None** — no park/saved-search symbols under `app/` | `rg` over `app/**/*.py` for saved/park/search_mem/mnemonic → no matches; tables in `fdf8821871d7_main_tables.py` are users/followers/articles/tags/favorites/comments only |

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | Package chassis / `app/` vs `src/` | Accepted — continue for INIT-003 unless superseded (resolves spec Q-08) |
| ADR-002 | Private-shelf `favorited=` authorization | Accepted — INIT-001 favorites shelf; **out of** INIT-003 CAP scope (pattern reference only) |
| ADR-003 | Public `favoritesCount` wire policy | Accepted — INIT-001; out of scope |
| ADR-004 | Unseat via client JWT discard | Accepted — supports REQ-08 / REQ-12 (logout drops seat, not park rows) |
| ADR-005 | Idempotent subscribe wire | Accepted — INIT-002; out of scope |
| ADR-006 | Guest `following` omit | Accepted — INIT-002; out of scope |

Accepted ADR constraint set for F13: **ADR-001**, **ADR-004** (load-bearing). No NEW-ADR candidate clears the qualification rubric for this greenfield private retention object (persistence/route encoding are ordinary TDD choices bounded by ADR-001 + repository/migration rules).

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout, JWT verify, `src/` packages, service naming | read — chassis exception via ADR-001 |
| `dependency-injection.mdc` | injector lifecycle | skim — chassis-tied; Wave0a uses FastAPI Depends |
| `infra-services.mdc` | DB / outbound clients | skim |
| `repository-pattern.mdc` | repo ↔ ORM boundary | read — new parks repo expected under `app/db/repositories/` |
| `pydantic-schemas.mdc` | models in `src/models/` | read — baseline uses `app/models` under ADR-001 |
| `http-api-conventions.mdc` | body vs query | read — park/relabel writes as body models |
| `fail-fast.mdc` | no silent fallbacks | read — empty/whitespace refuse; missing id fail-closed |
| `testing-verify-flows.mdc` | verify / pytest split | read — F3 harness gap |
| `python-tooling.mdc` | make check / pyright | skim |
| `database-migrations.mdc` | Alembic scripts | read — new parks table via create script |
| `strong-typing.mdc` | typing boundaries | skim |
| `python-imports.mdc` | import policy | skipped — N/A to product seams |
| `logging-loguru.mdc` | structured logging | skipped — NFR observability N/A as kill criterion |
| `spec-driven-development.mdc` | SDD discipline | skim |
| `code-guidelines-index.mdc` | index | skim |

## Traceability matrix

| Spec REQ / wave | Spec claim | Code evidence | Unit | Verify | Status |
|-----------------|------------|---------------|------|--------|--------|
| REQ-01 / CAP-01 | Park with label | none found — new capability | planned | planned | gap |
| REQ-02 / CAP-01 | Park without / blank label | none found — new capability | planned | planned | gap |
| REQ-03 / CAP-01 | Refuse empty/whitespace query | none found — new capability | planned | planned | gap |
| REQ-04 / CAP-03 | Refuse park while unseated | Seat gate reusable: `get_current_user_authorizer()` in `app/api/dependencies/authentication.py`; no park route yet | partial (auth) | planned | gap |
| REQ-05 / CAP-02 | Own-recall with query fidelity | none found — new capability | planned | planned | gap |
| REQ-06 / CAP-02 | Relabel (incl. clear) | none found — new capability | planned | planned | gap |
| REQ-07 / CAP-02 | Discard owned park | none found — new capability | planned | planned | gap |
| REQ-08 / CAP-02 | Persist across unseat/reseat | Durable store absent; unseat = client JWT discard (ADR-004); no logout wipe path | gap | planned | gap |
| REQ-09 / CAP-02 | Empty own-recall after last discard | none found — new capability | planned | planned | gap |
| REQ-10 / CAP-03 | Peer opacity | none found — new capability (favorites ownership is separate object) | planned | planned | gap |
| REQ-11 / CAP-03 | Peer mutate denied | none found — new capability | planned | planned | gap |
| REQ-12 / CAP-03 | Unseated list/relabel/discard denied | Auth required pattern exists; no park routes | partial (auth) | planned | gap |
| REQ-13 / CAP-03 | Missing/non-owned → indist. not-found | `EntityDoesNotExist` pattern in `app/db/errors.py` / route handlers; no park identity yet | planned | planned | gap |
| REQ-14 / CAP-02 | Newest-first by park time | none found — new capability | planned | planned | gap |
| REQ-15 / CAP-01/02 | Duplicate queries / non-unique labels | none found — new capability | planned | planned | gap |
| REQ-16 / CAP-02 | Query immutable after park | none found — new capability (no query-edit path to remove) | planned | planned | gap |
| Seat baseline (A-01) | Login seats / omit-bearer unseats | `app/api/routes/authentication.py`, JWT via `app/services/jwt.py`; ADR-004 | exists | planned | exists |
| Favorites residual | INIT-001 shelf not reopened | `favorites` table + `ArticlesRepository` favorite helpers | exists (OOS) | N/A | residual OOS |
| Follow residual | INIT-002 not reopened | `followers_to_followings` + `profiles.py` | exists (OOS) | N/A | residual OOS |

## ADR traceability (F13)

| Spec REQ / wave | Relevant ADR(s) | Status | Code evidence | Finding |
|-----------------|-----------------|--------|----------------|---------|
| CAP-01..03 / Q-08 chassis | ADR-001 | aligned | `app/main.py`, `app/api/routes/api.py`; no `src/` tree | N/A — continue Accepted Option A (`app/`); supersede only if INIT-003 migrates to `src/` |
| REQ-08 / REQ-12 unseat | ADR-004 | aligned | no logout route; JWT via `app/services/jwt.py`; parks will be membership-scoped DB rows (greenfield) | N/A — client discard unseats without wiping owner-private retention |
| Isolation pattern (analogy) | ADR-002 | N/A (different object) | `favorites` join + favorited-filter gate | N/A — do not reopen favorites; parks are a separate retention object |
| Parks persistence / routes | N/A | ordinary eng (no NEW-ADR) | none found — new capability; nearest patterns `app/db/migrations/versions/fdf8821871d7_main_tables.py` (`favorites`), `app/db/repositories/` | Ordinary TDD: dedicated owner-scoped table + new router under ADR-001 — not an ADR fork |

## Governance findings (F13–F14)

| ID | Check | Spec quote | Governing doc | Finding |
|----|-------|------------|---------------|---------|
| FF-04 | F14 | "How to introduce park persistence and stewardship routes on the legacy Conduit `app/` baseline vs platform `src/` chassis for CAP-01..CAP-03" | ADR-001 / `architecture.mdc` | Spec Q-08 still frames chassis as open; Accepted ADR-001 already locks Wave0a `app/` retention — cite ADR-001 and mark Q-08 resolved (auto-fix; not blocking) |

## Findings by severity

### Critical

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| — | — | none | — |

### Should fix

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| — | — | none | — |

### Verify / Gap (informational)

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| FF-01 | F1 / F3 | No `tests/verify/` / `tests/README.md`; live CAP/J coverage planned only | Spec evidence layers cite live CAP/J; Makefile curl-only `verify` |
| FF-02 | F5 | As-built index absent — cannot assert live maturity for CAP-01..03 | Empty `docs/specification/as-built/`; spec A-07 |
| FF-03 | F2 / F4 | CAP-01..CAP-03 entirely greenfield — park table, routes, repo, schemas, and unit/live cases do not exist yet | `rg` no park/saved-search under `app/`; migration has no parks table; no `tests/test_*` park modules |
| FF-04 | F14 / auto-fix | Spec Q-08 still open while Accepted ADR-001 resolves chassis to continue `app/` | Spec Q-08; `docs/specification/adr/adr-001-wave0a-package-chassis.md` |

## Impact surface

| Wave / area | Likely files/modules | Test touch |
|-------------|----------------------|------------|
| CAP-01 park create + empty refuse | New router under `app/api/routes/`; mount in `app/api/routes/api.py`; schemas under `app/models/`; validation refuse whitespace | unit create/label/empty; live J-01, J-02, J-12 |
| CAP-02 recall / relabel / discard / order / immutability | New repository + SQL under `app/db/`; Alembic revision via `scripts/create_postgres_migration.sh` (or Wave0a Alembic path under `app/db/migrations/`) | unit list/order/relabel/clear/discard/empty; live J-03..J-05, J-10 |
| CAP-03 isolation + unseated denials | Reuse `get_current_user_authorizer()`; owner-scoped queries; indist. not-found via `EntityDoesNotExist` | unit peer/unseated/missing id; live J-06, J-07, J-09, J-11 |
| Durability across reseat | Membership FK to `users`; ADR-004 unseat (omit bearer) | live J-08 |
| Harness | `tests/verify/*`, `tests/README.md`, as-built index | live kill paths; CI vs live docs |
| Chassis | Stay under `app/**` per ADR-001 | N/A migrate |

## Risks & assumptions

| ID | Risk / assumption | Mitigation |
|----|-------------------|------------|
| R-01 | Greenfield parks surface slips into web UI or auto-run scope | Keep non-goals / deferred web+local; prove API-only |
| R-02 | Peer harvest via guessed park ids if not-found vs forbidden diverge | REQ-13 indist. not-found; match existing `EntityDoesNotExist` polarity |
| R-03 | Session-only memory if parks stored in-process | Persist in Postgres under ownership FK; prove J-08 |
| R-04 | A-07 as-built absent — maturity unknown beyond this scan | Publish as-built rows at ground / first wave |
| A-01 (spec) | INIT-001 seat semantics remain the gate | Confirmed via authentication + ADR-004 |
| A-05 (spec) | Durable retention across logout/login | DB rows + JWT discard unseat |
| IM-04 / Q-04 | Eng reasonableness limits for count/lengths | TDD names limits; blank label = no label (REQ-02) |

## Recommended spec edits

- Mark **Q-08 resolved** citing **Accepted ADR-001** (continue `app/`) so chassis is not re-litigated unless a superseding ADR is opened.
- Optionally name planned verify module(s) once the implementation plan lands (do not invent coverage markers here).
- Do **not** expand this INIT into settings UI, auto-run, favorites, or subscription rules.

---

## Open items by lane

> Routing rubric: product scope / UX → PM · engineering decisions / ADR → PE ·
> business source-of-truth → Domain SME · naming drift / inferred fixes → Auto-fix.
> Full rubric: `skills/development/spec-technical-review/references/governance.md`
> (in this pin; not a workspace-relative `.agents/skills/…` path).

This table is the canonical open-item handoff. The lane-specific sections
below may add narrative but must not contradict it.

| ID | Lane | Question / item | Blocking | Owner | Status | Required by | Default if deferred | Evidence | Resolution reference |
|----|------|-----------------|----------|-------|--------|-------------|---------------------|----------|----------------------|
| Q-01 | PM | Query edit after park? (OQ-01 / IM-01) | no | PM | resolved | feasibility | Relabel + discard only; query immutable | REQ-16 | Impact-Map IM-01 → REQ-16 |
| Q-02 | PM | Auto-run parked query? (OQ-02 / IM-02) | no | PM | resolved | later | Re-presentable text enough | Out of scope | Impact-Map IM-02 |
| Q-03 | PM | Missing vs non-owned fail shape (OQ-03 / IM-03) | no | PM | resolved | feasibility | Indistinguishable not-found | REQ-13 | Impact-Map IM-03 → REQ-13 |
| Q-04 | PM | Max parks / lengths (OQ-04 / IM-04) | no | PM | resolved | feasibility | Eng reasonableness; blank label = none | REQ-02; NFR Performance | Impact-Map IM-04 |
| Q-05 | PM | Recall ordering (OQ-05 / IM-05) | no | PM | resolved | feasibility | Newest-first by park time | REQ-14 | Impact-Map IM-05 → REQ-14 |
| Q-06 | PM | Duplicate queries / unique labels (OQ-06 / IM-06) | no | PM | resolved | feasibility | Duplicates allowed; labels not unique | REQ-15 | Impact-Map IM-06 → REQ-15 |
| Q-07 | PM | Clear label to none (OQ-07 / IM-07) | no | PM | resolved | feasibility | Allowed without discard | REQ-06 | Impact-Map IM-07 → REQ-06 |
| Q-08 | PE | Chassis `app/` vs `src/` for park surface | no | PE | resolved | technical review | Continue Accepted ADR-001 Option A | ADR-001; `app/` | `docs/specification/adr/adr-001-wave0a-package-chassis.md` |
| FF-01 | auto-fix | Add `tests/verify` + `tests/README.md` when plan names scripts | no | PE | open | plan | Document verify commands per CAP/J | F3 | pending plan |
| FF-02 | auto-fix | Seed as-built index rows as gap until waves close | no | PE | open | ground / first wave | Index rows = not implemented | F5 / A-07 | pending |
| FF-03 | auto-fix | Plan greenfield parks modules (table/routes/repo/tests) | no | PE | open | plan / technical review | Dedicated owner-scoped table under `app/` | F2 gap matrix | pending TDD/plan |
| FF-04 | auto-fix | Spec Q-08 still open vs ADR-001 Accepted | no | PE | open | Forge publish / next spec edit | Mark Q-08 resolved citing ADR-001 | Spec Q-08; ADR-001 | pending authorized edit |

### PM questions (product scope, UX, priority)

#### Blocking — must resolve before spec merge
*(none — IM/OQ defaults already locked into REQs)*

#### Defer — can proceed with documented assumption
1. OQ-02 / IM-02 auto-run — deferred later / non-goal (non-blocking).
2. OQ-04 length/count ceilings — eng reasonableness in TDD (non-blocking).

### PE questions (engineering decisions — resolved by `/spec-technical-review`)

> These are **not** for PM. Run `/spec-technical-review` to produce a Technical
> Design Document that resolves these before `/spec-implementation-plan`.

#### Blocking for implementation plan
*(none — outcome `pass`)*

#### Defer with default
1. Q-08 chassis — **resolved**: continue Accepted ADR-001 (`app/`).
2. Parks persistence encoding (dedicated table vs alternate) — ordinary TDD under repository/migration rules; default dedicated owner-scoped Postgres table analogous to `favorites` ownership, not NEW-ADR.
3. Route path / park identity encoding — ordinary TDD (no CTR this INIT); keep out of product REQ text.
4. Eng reasonableness limits (IM-04) — name in TDD/plan without inventing product caps.

### Domain clarifications (business source-of-truth)

| # | Question | Suggested SME | Blocks |
|---|----------|---------------|--------|
| — | none | — | — |

### Auto-fixable (agent resolves later — not inside this skill)

| # | Item | Fix |
|---|------|-----|
| AF-1 | Missing `tests/README.md` / `tests/verify` scaffolding | Add when plan names verify scripts and covers markers |
| AF-2 | Empty as-built index | Seed capability rows as gap after first wave / at ground |
| AF-3 | Greenfield parks surface | Plan table + router + repo + unit/live under `app/` per ADR-001 |
| AF-4 | Q-08 open in product spec vs ADR-001 Accepted | Spec edit to mark Q-08 resolved citing ADR-001 (recommended; not applied in this read-only pass) |

---

## Check summary

| Check | Status | Findings |
|-------|--------|----------|
| F1 Baseline snapshot | PASS | Harness partial; as-built absent (FF-01/FF-02 informational) |
| F2 Spec → code map | PASS | All CAP/REQ mapped; greenfield gaps expected (FF-03 informational); seat/auth baseline exists |
| F3 Spec → verify map | PASS | Planned under `tests/verify` (FF-01 informational) |
| F4 Spec → unit map | PASS | Planned under existing `tests/test_api/` layout (profile `tests/unit` absent — same as siblings) |
| F5 As-built drift | PASS | No false “live” claims; A-07 notes absence (FF-02) |
| F6 Docs drift | PASS | AGENTS/rules/ADR present; README lists INIT-003 Draft |
| F7 Overlap risk | PASS | No park unit/live yet — no duplicate journey ownership |
| F8 CI vs live boundary | PASS | Pytest local/CI; Makefile curl verify; SDD verify not yet |
| F9 Cross-service touch | PASS | None — PRD §8 / impact-map §6 / spec Cross-service contracts |
| F10 Assumptions | PASS | A-01..A-06 confirmed; A-07 open PE (as-built) informational |
| F11 Effort drivers | PASS | New table/routes/repo; auth reuse; verify harness; isolation prove |
| F12 PM questions | PASS | Zero blocking PM |
| F13 ADR conformance | PASS | ADR-001/004 aligned; no NEW-ADR; no Accepted-ADR conflict |
| F14 MDC conformance | PASS | Chassis exception Accepted via ADR-001 (FF-04 informational auto-fix) |

**Check PASS** = zero unresolved blocking findings (informational OK).

**Overall:** PASS → workflow outcome `pass`.

---

## Next steps

> Persist this report locally alongside the spec draft. Fill `handoff.forge` for
> `/commit-workspace` (or Gateflow ForgeClient) onto the Draft spec PR —
> **do not** commit, push, open PRs, or apply labels inside this skill.
> The spec PR is the engineering review surface; product Q&A uses the meta PRD PR.

**PM questions** → post as numbered comments on the **meta PRD PR** (plain English).
  Link from a spec PR comment if helpful. PM answers on meta PRD PR.
  Unresolved blocking PM items → outcome `needs-input`.

**PE questions** → discuss on the **Draft spec PR**; run `/spec-technical-review` next.
  PE accepts TDD/ADRs in **files** (`Draft` → `Accepted`); do **not** set
  `spec-lgtm` until the full package includes the implementation plan.
  Unresolved blocking PE/ADR items → outcome `findings`.

**Domain clarifications** → meta PRD PR comment or tracked issue; record answers in
  `open-questions.md` and publish via Forge to the spec branch.
  Unresolved blocking domain items → outcome `needs-input`.

**Auto-fixable items** → leave in report; resolve in a later authorized edit —
  not during this read-only feasibility run.

### Forge readiness

| Item | Value |
|------|-------|
| Local report path | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md` |
| Target branch | `chore/INIT-REALWORLD-003-spec-realworld-api` (Draft spec PR not open yet) |
| Recommended forge | `/commit-workspace` (Gate 2 stays `spec-pending`) |
| Mutations performed by this skill | **none** |

```
Draft spec PR: chore/INIT-REALWORLD-003-spec-realworld-api  (spec-pending) — not opened yet
When ready:
  [x] Source freshness is CURRENT
  [x] All blocking PM questions answered (IM defaults locked into REQs)
  [x] All blocking Domain clarifications answered (none)
  [ ] Spec updated to cite ADR-001 for Q-08 (recommended AF-4; same branch via Forge)
  [x] This /initiative-feasibility pass is clean (outcome pass)
  [ ] Proceed: /spec-technical-review (always — pin routes pass and findings here)
  [ ] After spec + feasibility + TDD (if any) + plan on branch (Forge publish):
      PE sets spec-lgtm + Approve on exact head → Ready for review → merge
  [ ] After merge: `/create-board-tickets` from plan §9 — then /pre-implement → /loop-spec
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: initiative-feasibility
  outcome: pass
  artifact:
    path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8
    scope_digest: sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7
    meta_pr_approved_head: abfbbcff877a83c298776fd4801b8ac4c75ddfba
    ripple_action: continue
    new_adr: false
    new_adr_ids: []
    draft_adr_paths: []
    lane_counts:
      pm_blocking_open: 0
      pe_blocking_open: 0
      domain_blocking_open: 0
      auto_fix_open: 4
    severity_counts:
      critical: 0
      should_fix: 0
      verify_gap: 4
    draft_spec_pr: none
    codegraph_provider: degraded-none
    grounding_depth: none
    outcome_rationale: zero unresolved blocking findings; greenfield CAP gaps and harness/as-built observations are informational only
  next_candidates:
    - spec-technical-review
  human_checkpoint: false
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-003] Spec — realworld-api (feasibility)"
    body_path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md
    target_branch: chore/INIT-REALWORLD-003-spec-realworld-api
```
