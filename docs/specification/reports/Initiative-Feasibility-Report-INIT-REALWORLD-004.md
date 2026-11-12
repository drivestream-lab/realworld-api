# Feasibility report — INIT-REALWORLD-004

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-004 |
| Spec | `docs/specification/product/INIT-REALWORLD-004-api.md` |
| PRD digest | `sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-004.md` / `1` |
| Repo scope digest | `sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5` |
| Approved meta PR head | `02c74d94cf8748c1cd53a268035a8a84433caf94` |
| Impact-map approval | Review `PRR_kwDOVac9Rs8AAAABXCxxnw` / id `5841383839` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T11:55:48Z`; `commit_id` = `02c74d94cf8748c1cd53a268035a8a84433caf94` (meta PR [#12](https://github.com/drivestream-lab/realworld-meta/pull/12) MERGED; label `impact-map-lgtm`) |
| Source freshness | CURRENT — H1 live PRD digest matches spec citation; H2 api scope digest recomputed match (`capabilities=CAP-01,CAP-02,CAP-03,REQ-01..REQ-18`); H3 `map_revision=1`; G1 APPROVED review `commit_id` equals merged meta PR #12 head; ripple `continue` |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Branch | `chore/INIT-REALWORLD-004-spec-realworld-api` — proposed Draft spec PR branch (none open yet; Gate 2 stays `spec-pending`) |
| Initiative segment | `INIT-REALWORLD-004` |
| Status | Draft |
| Review deadline | 2026-11-17 |
| Deciders | PM: programme PM · Domain SME: @drivestream-lab/backend-devs |
| Re-run note | Hermes non-interactive first feasibility pass against live PRD/map/G1 and `app/` evidence; Q-11 chassis locked to continue Accepted ADR-001 Option A |

## Summary

INIT-REALWORLD-004 is **buildable** on the Accepted Wave0a Conduit baseline under `app/`: CAP-01..CAP-03 are a **greenfield** membership→tag follow-edge surface (no tag-follow tables or stewardship routes today), while seat gating and durable membership retention reuse existing JWT seat + Postgres patterns (ADR-001 / ADR-004). Author-follow (`profiles` / `followers_to_followings`) and public tag catalog (`tags`) remain residual baselines and must not be reused as the tag-edge store. Source freshness is **CURRENT**. Zero unresolved blocking PM/PE/ADR findings — IM defaults are locked into REQ-01..REQ-22; chassis Q-11 defaults to Accepted ADR-001. Proceed to `/spec-technical-review` (outcome `pass`); do not set `spec-lgtm`.

**Findings:** 3 total (0 Critical, 0 Should fix, 3 Verify / Gap)

### Derived counts (lane × severity)

| Lane | Blocking open | Non-blocking open | Resolved |
|------|---------------|-------------------|----------|
| PM | 0 | 4 (Q-07..Q-10 later) | 6 (Q-01..Q-06 / IM-01..IM-06 → REQs/NFR) |
| PE / ADR | 0 | 0 | 1 (Q-11 chassis → cite Accepted ADR-001 continue `app/`) |
| Domain | 0 | 0 | 0 |
| Auto-fix | 0 | 3 | 0 |

| Severity | Unresolved count |
|----------|------------------|
| Critical | 0 |
| Should fix | 0 |
| Verify / Gap (informational) | 3 |

### Selected workflow outcome

| Field | Value |
|-------|-------|
| Outcome | `pass` |
| Rationale | Zero unresolved blocking findings; informational Verify/Gap (harness, as-built, greenfield gaps) may remain |
| Next (from workflow) | `spec-technical-review` |

Informational observations alone do **not** select `findings`. Unresolved
blocking PE/ADR → `findings`; blocking PM/domain → `needs-input`.

## Baseline snapshot (F1)

| Area | Current state | Evidence |
|------|---------------|----------|
| Unit / in-process tests | Present under `tests/test_api/`, `tests/test_services/`, `tests/test_schemas/`, `tests/test_db/` (not `tests/unit/`). Auth, users, articles/favorites, profiles/author-follow, tags catalog covered. **No** membership→tag follow-edge tests. | `tests/test_api/test_routes/test_login.py`, `test_articles.py`, `test_profiles.py`, `test_tags.py`; `pyproject.toml` |
| Live verify | **Absent** as SDD `tests/verify/` + `tests/README.md`. Makefile `verify` is a single host curl to `localhost:3100/api/articles`. | `Makefile` `verify` target; no `tests/verify/`; no `tests/README.md` |
| As-built | **Absent** — `docs/specification/as-built/` missing | Spec A-10; empty/missing as-built dir |
| Source layout | Legacy Conduit package under `app/` (routes, asyncpg repos, Alembic). **No** `src/` tree. Covered by Accepted ADR-001 Option A. | `app/main.py`, `app/api/routes/api.py`; ADR-001 |
| Toolchain | Poetry; black; pytest; Makefile `verify` only (no `make check` / pyright / import-linter yet) | `pyproject.toml`, `Makefile` |
| ADRs | ADR-001..004 **Accepted** (INIT-001). No INIT-004 ADRs yet — none required at feasibility. | `docs/specification/adr/adr-001-*.md` … `adr-004-*.md` (Status: Accepted) |
| Tag-follow surface | **None** — author-follow + public tags exist; no membership→tag follow-edge tables/routes | `rg` over `app/**/*.py` for tag-follow/followed_tag → no matches; `profiles.py` is author follow only; `tags.py` is public catalog GET; migration tables are users/followers/articles/tags/favorites/comments only |

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | Package chassis / `app/` vs `src/` | Accepted — continue for INIT-004 unless superseded (resolves spec Q-11) |
| ADR-002 | Private-shelf `favorited=` authorization | Accepted — INIT-001 favorites shelf; **out of** INIT-004 CAP scope (pattern reference only) |
| ADR-003 | Public `favoritesCount` wire policy | Accepted — INIT-001; out of scope |
| ADR-004 | Unseat via client JWT discard | Accepted — supports REQ-05 / REQ-02 / REQ-09 (logout drops seat, not tag-follow edges) |

Accepted ADR constraint set for F13: **ADR-001**, **ADR-004** (load-bearing). No NEW-ADR candidate clears the qualification rubric for this greenfield private edge object (persistence/route encoding are ordinary TDD choices bounded by ADR-001 + repository/migration rules). Do **not** reuse `followers_to_followings` as the tag-edge store.

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout, JWT verify, `src/` packages, service naming | read — chassis exception via ADR-001 |
| `dependency-injection.mdc` | injector lifecycle | skim — chassis-tied; Wave0a uses FastAPI Depends |
| `infra-services.mdc` | DB / outbound clients | skim |
| `repository-pattern.mdc` | repo ↔ ORM boundary | read — new tag-follow repo expected under `app/db/repositories/` |
| `pydantic-schemas.mdc` | models in `src/models/` | read — baseline uses `app/models` under ADR-001 |
| `http-api-conventions.mdc` | body vs query | read — establish/dissolve writes as body models |
| `fail-fast.mdc` | no silent fallbacks | read — empty/whitespace refuse; missing edge fail-closed |
| `testing-verify-flows.mdc` | verify / pytest split | read — F3 harness gap |
| `python-tooling.mdc` | make check / pyright | skim |
| `database-migrations.mdc` | Alembic scripts | read — new tag-follow table via create script |
| `strong-typing.mdc` | typing boundaries | skim |
| `python-imports.mdc` | import policy | skipped — N/A to product seams |
| `logging-loguru.mdc` | structured logging | skipped — NFR observability N/A as kill criterion |
| `spec-driven-development.mdc` | SDD discipline | skim |
| `code-guidelines-index.mdc` | index | skim |

## Traceability matrix

| Spec REQ / wave | Spec claim | Code evidence | Unit | Verify | Status |
|-----------------|------------|---------------|------|--------|--------|
| REQ-01 / CAP-01 | Establish membership→tag follow edge by name | none found — new capability | planned | planned | gap |
| REQ-02 / CAP-03 | Refuse establish while unseated | Seat gate reusable: `get_current_user_authorizer()` in `app/api/dependencies/authentication.py`; no tag-follow route yet | partial (auth) | planned | gap |
| REQ-03 / CAP-02 | Own outgoing list with name fidelity | none found — new capability | planned | planned | gap |
| REQ-04 / CAP-02 | Dissolve owned outgoing edge | none found — new capability | planned | planned | gap |
| REQ-05 / CAP-02 | Persist across unseat/reseat | Durable store absent; unseat = client JWT discard (ADR-004); no logout wipe path | gap | planned | gap |
| REQ-06 / CAP-02 | Empty own-list after last dissolve | none found — new capability | planned | planned | gap |
| REQ-07 / CAP-03 | Peer opacity on outgoing edges | none found — new capability (author-follow is a different graph) | planned | planned | gap |
| REQ-08 / CAP-03 | Peer dissolve denied | none found — new capability | planned | planned | gap |
| REQ-09 / CAP-03 | Unseated list/unfollow denied | Auth required pattern exists; no tag-follow routes | partial (auth) | planned | gap |
| REQ-10 / CAP-03 | Missing/non-owned → indist. not-found | `EntityDoesNotExist` pattern in `app/db/errors.py` / route handlers; no tag-edge identity yet | planned | planned | gap |
| REQ-11 / CAP-01 | Refuse empty/whitespace tag name | none found — new capability | planned | planned | gap |
| REQ-12 / CAP-03 | Public tag-lane independent of edges | Public tag filter exists (`articles` tag query); no personalization hook from tag-follow (surface absent) | residual OOS | planned | gap (prove non-rewrite) |
| REQ-13 / CAP-02 | Re-establish after dissolve | none found — new capability | planned | planned | gap |
| REQ-14 / CAP-03 | Subscription stream independent of tag edges | Author-follow feed via `followers_to_followings` in `articles.sql`; must not compose with tag edges | residual OOS | planned | gap (prove non-composition) |
| REQ-15 / CAP-02 | Distinct from parked search | Park surface not present in this checkout; favorites residual separate | residual OOS | planned | gap (prove separation when parks land) |
| REQ-16 / CAP-03 | Peer/guest public lane unaffected | Public tag lane ungated today (`tags.py` + article tag filter) | residual | planned | gap (prove) |
| REQ-17 / CAP-03 | Concurrent same-tag independence | none found — new capability (membership-scoped rows required) | planned | planned | gap |
| REQ-18 / CAP-03 | No inbound followers-of-tag | No reverse-index route today; must not add one | none (absence is correct) | planned | gap (prove absence) |
| REQ-19 / CAP-01 | Establish to corpus-empty tag name | Public `tags` table is article-linked; edge store must not require existing tag row (OQ-01 default) | planned | planned | gap |
| REQ-20 / CAP-01 | Idempotent re-follow | none found — new capability | planned | planned | gap |
| REQ-21 / CAP-02 | Newest-established-first list order | none found — new capability | planned | planned | gap |
| REQ-22 / CAP-01/02 | Trim + case-sensitive identity | none found — new capability | planned | planned | gap |
| Seat baseline (A-01) | Login seats / omit-bearer unseats | `app/api/routes/authentication.py`, JWT via `app/services/jwt.py`; ADR-004 | exists | planned | exists |
| Author-follow residual | INIT-002 not reopened | `followers_to_followings` + `app/api/routes/profiles.py` | exists (OOS) | N/A | residual OOS |
| Public tags residual | INIT-001 tag catalog / lanes | `tags` + `articles_to_tags`; `app/api/routes/tags.py` | exists (OOS) | N/A | residual OOS |
| Favorites residual | INIT-001 shelf not reopened | `favorites` table + article favorite helpers | exists (OOS) | N/A | residual OOS |

## ADR traceability (F13)

| Spec REQ / wave | Relevant ADR(s) | Status | Code evidence | Finding |
|-----------------|-----------------|--------|----------------|---------|
| CAP-01..03 / Q-11 chassis | ADR-001 | aligned | `app/main.py`, `app/api/routes/api.py`; no `src/` tree | N/A — continue Accepted Option A (`app/`); supersede only if INIT-004 migrates to `src/` |
| REQ-05 / REQ-02 / REQ-09 unseat | ADR-004 | aligned | no logout route; JWT via `app/services/jwt.py`; tag-follow edges will be membership-scoped DB rows (greenfield) | N/A — client discard unseats without wiping owner-private retention |
| Isolation pattern (analogy) | ADR-002 | N/A (different object) | `favorites` join + favorited-filter gate | N/A — do not reopen favorites; tag-follow is a separate edge object |
| Tag-follow persistence / routes | N/A | ordinary eng (no NEW-ADR) | none found — new capability; nearest patterns `app/db/migrations/versions/fdf8821871d7_main_tables.py` (`favorites`, `followers_to_followings`, `tags`); `app/db/repositories/`; `app/api/routes/profiles.py` (author-follow — **do not reuse**) | Ordinary TDD: dedicated owner-scoped membership→tag edge table + new router under ADR-001 — not an ADR fork |

## Governance findings (F13–F14)

| ID | Check | Spec quote | Governing doc | Finding |
|----|-------|------------|---------------|---------|
| — | F13 | — | — | none — no NEW-ADR / no Accepted-ADR conflict |
| — | F14 | — | — | none — chassis exception Accepted via ADR-001; greenfield tag-follow does not conflict with matched MDC domains |

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
| FF-02 | F5 | As-built index absent — cannot assert live maturity for CAP-01..03 | Missing `docs/specification/as-built/`; spec A-10 |
| FF-03 | F2 / F4 | CAP-01..CAP-03 entirely greenfield — tag-follow table, routes, repo, schemas, and unit/live cases do not exist yet; must stay distinct from author-follow | `rg` no tag-follow under `app/`; migration has no membership→tag edge table; author-follow only in `profiles.py` / `followers_to_followings`; no `tests/test_*` tag-follow modules |

## Impact surface

| Wave / area | Likely files/modules | Test touch |
|-------------|----------------------|------------|
| CAP-01 establish + empty refuse + trim/idempotency | New router under `app/api/routes/`; mount in `app/api/routes/api.py`; schemas under `app/models/`; validation refuse whitespace | unit create/empty/trim/idempotent; live J-01, J-02, J-11, J-13 |
| CAP-02 list / dissolve / order / durability | New repository + SQL under `app/db/`; Alembic revision via Wave0a Alembic path under `app/db/migrations/` (create-script discipline) | unit list/order/dissolve/empty; live J-03, J-04, J-08, J-10, J-13, J-15 |
| CAP-03 isolation + unseated denials + anti-reciprocity + non-composition | Reuse `get_current_user_authorizer()`; owner-scoped queries; indist. not-found via `EntityDoesNotExist`; **no** inbound followers-of-tag route; do not rewrite article tag filter or author-feed SQL | unit peer/unseated/missing; live J-05..J-07, J-09, J-12, J-14, J-16..J-18 |
| Durability across reseat | Membership FK to `users`; ADR-004 unseat (omit bearer) | live J-08 |
| Harness | `tests/verify/*`, `tests/README.md`, as-built index | live kill paths; CI vs live docs |
| Chassis | Stay under `app/**` per ADR-001; do not reuse `followers_to_followings` | N/A migrate |

## Risks & assumptions

| ID | Risk / assumption | Mitigation |
|----|-------------------|------------|
| R-01 | Greenfield tag-follow slips into author-follow tables or web UI | Keep non-goals / deferred web+local; dedicated edge table; prove API-only |
| R-02 | Peer harvest via guessed identities if not-found vs forbidden diverge | REQ-10 indist. not-found; match existing `EntityDoesNotExist` polarity |
| R-03 | Session-only memory if edges stored in-process | Persist in Postgres under ownership FK; prove J-08 |
| R-04 | Accidental composition with author-follow feed or public tag personalization | REQ-12/14/16/18 prove paths; no inbound reverse index |
| R-05 | A-10 as-built absent — maturity unknown beyond this scan | Publish as-built rows at ground / first wave |
| A-01 (spec) | INIT-001 seat semantics remain the gate | Confirmed via authentication + ADR-004 |
| A-03 (spec) | Durable retention across logout/login | DB rows + JWT discard unseat |
| IM-04 / Q-04 | Eng reasonableness limits for count/lengths | TDD names limits without inventing product caps |

## Recommended spec edits

- Optionally cite Accepted ADR-001 on Q-11 in the product-spec tip (chassis already defaulted; feasibility locks continue `app/`).
- Optionally name planned verify module(s) once the implementation plan lands (do not invent coverage markers here).
- Do **not** expand this INIT into settings UI, feed personalization, inbound followers-of-tag, author-follow reuse, or parks rewrite.
- Keep README INIT-004 row accurate until Draft spec PR opens via Forge.

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
| Q-01 | PM | Corpus-empty tag establish? (OQ-01 / IM-01) | no | PM | resolved | feasibility | Allow any non-empty normalized name | REQ-19 | Impact-Map IM-01 → REQ-19 |
| Q-02 | PM | Idempotent re-follow vs conflict? (OQ-02 / IM-02) | no | PM | resolved | feasibility | Idempotent success — list shows once | REQ-20 | Impact-Map IM-02 → REQ-20 |
| Q-03 | PM | Missing vs non-owned fail shape (OQ-03 / IM-03) | no | PM | resolved | feasibility | Indistinguishable not-found | REQ-10 | Impact-Map IM-03 → REQ-10 |
| Q-04 | PM | Max edges / tag-name length (OQ-04 / IM-04) | no | PM | resolved | feasibility | Eng reasonableness limits | NFR Performance | Impact-Map IM-04 |
| Q-05 | PM | Outgoing-list ordering (OQ-05 / IM-05) | no | PM | resolved | feasibility | Newest-established-first | REQ-21 | Impact-Map IM-05 → REQ-21 |
| Q-06 | PM | Tag-name normalization (OQ-06 / IM-06) | no | PM | resolved | feasibility | Trim; case-sensitive after trim | REQ-22 | Impact-Map IM-06 → REQ-22 |
| Q-07 | PM | Viewer-relative following CTA on public tags? (OQ-07 / IM-07) | no | PM | open | later | No — private outgoing surface enough | Out of scope | Impact-Map IM-07 |
| Q-08 | PM | History of former follows after dissolve? (OQ-08 / IM-08) | no | PM | open | later | Fully removed; no history surface | Out of scope | Impact-Map IM-08 |
| Q-09 | PM | Favorites vs tag-follow mutual invisibility? (OQ-09 / IM-09) | no | PM | open | later | Separate surfaces; no cross-write | Out of scope | Impact-Map IM-09 |
| Q-10 | PM | Future reverse-index without new INIT? (OQ-10 / IM-10) | no | PM | open | later | No — later INIT required | REQ-18 | Impact-Map IM-10 |
| Q-11 | PE | Chassis `app/` vs `src/` for tag-follow surface | no | PE | resolved | technical review | Continue Accepted ADR-001 Option A; do not reuse author-follow tables | ADR-001; `app/` | Feasibility lock → `docs/specification/adr/adr-001-wave0a-package-chassis.md` |
| FF-01 | auto-fix | Add `tests/verify` + `tests/README.md` when plan names scripts | no | PE | open | plan | Document verify commands per CAP/J | F3 | pending plan |
| FF-02 | auto-fix | Seed as-built index rows as gap until waves close | no | PE | open | ground / first wave | Index rows = not implemented | F5 / A-10 | pending |
| FF-03 | auto-fix | Plan greenfield tag-follow modules (table/routes/repo/tests) distinct from author-follow | no | PE | open | plan / technical review | Dedicated owner-scoped membership→tag edge table under `app/` | F2 gap matrix | pending TDD/plan |

### PM questions (product scope, UX, priority)

#### Blocking — must resolve before spec merge
*(none — IM/OQ defaults already locked into REQs)*

#### Defer — can proceed with documented assumption
1. OQ-07 / IM-07 public tag CTA state — deferred later / non-goal (non-blocking).
2. OQ-08 / IM-08 follow history — deferred later / non-goal (non-blocking).
3. OQ-09 / IM-09 favorites cross-visibility — deferred later; separate surfaces default (non-blocking).
4. OQ-10 / IM-10 future reverse-index — deferred later; requires new INIT (non-blocking).
5. OQ-04 length/count ceilings — eng reasonableness in TDD (non-blocking).

### PE questions (engineering decisions — resolved by `/spec-technical-review`)

> These are **not** for PM. Run `/spec-technical-review` to produce a Technical
> Design Document that resolves these before `/spec-implementation-plan`.

#### Blocking for implementation plan
*(none — outcome `pass`)*

#### Defer with default
1. Q-11 chassis — **resolved**: continue Accepted ADR-001 (`app/`).
2. Tag-follow persistence encoding (dedicated membership→tag edge table vs alternate) — ordinary TDD under repository/migration rules; default dedicated owner-scoped Postgres table; **do not** reuse `followers_to_followings` — not NEW-ADR.
3. Route path / edge identity encoding — ordinary TDD (no CTR this INIT); keep out of product REQ text.
4. Eng reasonableness limits (IM-04) — name in TDD/plan without inventing product caps.
5. Whether REQ-19 stores tag names without requiring a row in public `tags` — ordinary TDD; product default allows corpus-empty names.

### Domain clarifications (business source-of-truth)

| # | Question | Suggested SME | Blocks |
|---|----------|---------------|--------|
| — | none | — | — |

### Auto-fixable (agent resolves later — not inside this skill)

| # | Item | Fix |
|---|------|-----|
| AF-1 | Missing `tests/README.md` / `tests/verify` scaffolding | Add when plan names verify scripts and covers markers |
| AF-2 | Empty as-built index | Seed capability rows as gap after first wave / at ground |
| AF-3 | Greenfield tag-follow surface | Plan dedicated edge table + router + repo + unit/live under `app/` per ADR-001; keep author-follow residual |

---

## Check summary

| Check | Status | Findings |
|-------|--------|----------|
| F1 Baseline snapshot | PASS | Harness partial; as-built absent (FF-01/FF-02 informational) |
| F2 Spec → code map | PASS | All CAP/REQ mapped; greenfield gaps expected (FF-03 informational); seat/auth + author-follow/public-tags residuals exist |
| F3 Spec → verify map | PASS | Planned under `tests/verify` (FF-01 informational) |
| F4 Spec → unit map | PASS | Planned under existing `tests/test_api/` layout (profile `tests/unit` absent — same as siblings) |
| F5 As-built drift | PASS | No false “live” claims; A-10 notes absence (FF-02) |
| F6 Docs drift | PASS | AGENTS/rules/ADR present; README INIT-004 tip accurate (awaiting Draft PR) |
| F7 Overlap risk | PASS | No tag-follow unit/live yet — no duplicate journey ownership |
| F8 CI vs live boundary | PASS | Pytest local/CI; Makefile curl verify; SDD verify not yet |
| F9 Cross-service touch | PASS | None — PRD §8 / impact-map §6 / spec Cross-service contracts |
| F10 Assumptions | PASS | A-01..A-09 confirmed; A-10 open PE (as-built) informational |
| F11 Effort drivers | PASS | New table/routes/repo; auth reuse; verify harness; isolation + non-composition prove |
| F12 PM questions | PASS | Zero blocking PM |
| F13 ADR conformance | PASS | ADR-001/004 aligned; no NEW-ADR; no Accepted-ADR conflict |
| F14 MDC conformance | PASS | Chassis exception Accepted via ADR-001; no MDC conflict on greenfield tag-follow |

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
| Local report path | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md` |
| Target branch | `chore/INIT-REALWORLD-004-spec-realworld-api` (Draft spec PR not open yet; Gate 2 stays `spec-pending`) |
| Recommended forge | `/commit-workspace` (Gate 2 stays `spec-pending`) |
| Mutations performed by this skill | **none** |

```
Draft spec PR: chore/INIT-REALWORLD-004-spec-realworld-api  (spec-pending; open via Forge if absent)
When ready:
  [x] Source freshness is CURRENT
  [x] All blocking PM questions answered (IM defaults locked into REQs)
  [x] All blocking Domain clarifications answered (none)
  [x] Spec Q-11 locked to Accepted ADR-001 continue app/ (feasibility)
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
    path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3
    scope_digest: sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5
    meta_pr_approved_head: 02c74d94cf8748c1cd53a268035a8a84433caf94
    ripple_action: continue
    new_adr: false
    new_adr_ids: []
    draft_adr_paths: []
    lane_counts:
      pm_blocking_open: 0
      pe_blocking_open: 0
      domain_blocking_open: 0
      auto_fix_open: 3
    severity_counts:
      critical: 0
      should_fix: 0
      verify_gap: 3
    draft_spec_pr: none
    proposed_branch: chore/INIT-REALWORLD-004-spec-realworld-api
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
    title: "[INIT-REALWORLD-004] Spec — realworld-api (feasibility)"
    body_path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md
    target_branch: chore/INIT-REALWORLD-004-spec-realworld-api
```
