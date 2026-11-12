# Technical Design Document — INIT-REALWORLD-003

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-003 |
| Spec | `docs/specification/product/INIT-REALWORLD-003-api.md` |
| Spec digest | `sha256:37ab4aeedbdb73440a00ea968545b6c15fe5e2fc51727e961844184f9568a1bd` |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md` |
| PRD digest | `sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-003.md` / `1` |
| Repo scope digest | `sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7` |
| Approved meta PR head | `abfbbcff877a83c298776fd4801b8ac4c75ddfba` |
| Source freshness | CURRENT — H1 live PRD digest `sha256:5cccf070…` recomputed match; H2 scope digest `sha256:6e1a5775…` / CAP-01..03 match; H3 `map_revision=1`; G1 APPROVED `commit_id` = meta PR #10 head `abfbbcff…`; feasibility tip continuous (`new_adr: false`, zero `ALTERNATIVE:` findings); AF-4 applied (Q-08 → ADR-001) |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Branch | `chore/INIT-REALWORLD-003-spec-realworld-api` (spec PR — TDD published via Forge) |
| Initiative segment | `INIT-REALWORLD-003` |
| Status | Accepted |
| Review deadline | 2026-11-19 |
| Deciders | PE: @drivestream-lab/backend-devs — explicit LGTM required, not approval by silence |
| Codegraph | degraded-none — grounded via direct `app/` reads (profile `source_roots` lists `src/` but Wave0a tree is `app/` per ADR-001) |
| Grounding depth | light |

---

## 1. Problem statement

CAP-01..CAP-03 need a new owner-scoped retention aggregate under the Accepted Wave0a chassis (`app/`, ADR-001): durable Postgres rows, HTTP stewardship routes gated by `get_current_user_authorizer()`, and mutate loads that resolve via owner-scoped repository get → `EntityDoesNotExist` → HTTP 404 (REQ-01..REQ-16). No park/saved-search symbols exist today; seat unseat remains client JWT discard (ADR-004) without wiping membership-scoped rows.

---

## 2. Module / package boundaries

| Module | Current state | Change | Owns |
|--------|---------------|--------|------|
| `app/api/routes/parks.py` | new | create — park / recall / relabel / discard | HTTP stewardship edge |
| `app/api/routes/api.py` | exists | extend — `include_router` for parks | Route mount |
| `app/api/dependencies/parks.py` | new | create — path load by id scoped to owner | Path → domain park |
| `app/models/domain/parks.py` | new | create | Domain park DTO |
| `app/models/schemas/parks.py` | new | create — create/relabel/list envelopes | Wire schemas |
| `app/db/repositories/parks.py` | new | create — owner-scoped CRUD | Persistence |
| `app/db/queries/tables.py` (+ SQL if used) | exists | extend — `parks` table descriptor | Query builder / SQL |
| `app/db/migrations/versions/*` | exists (`fdf8821871d7` baseline) | new Alembic revision — `parks` table | Schema evolution |
| `app/api/dependencies/authentication.py` | exists | unchanged reuse | Seat gate |
| `app/db/errors.py` (`EntityDoesNotExist`) | exists | unchanged reuse | Indist. not-found polarity |
| `tests/test_api/` / `tests/test_services/` / `tests/test_db/` | exists | extend — park unit modules | In-process proof |
| `tests/verify/` + `tests/README.md` | absent | create in plan (FF-01) | Live smoke |
| `docs/specification/as-built/` | absent | seed at ground / first wave (FF-02) | Maturity index |
| `src/` | absent | **not** introduced (continue ADR-001 / Q-08) | N/A |

**Code grounding (T2 — this pass):**
- `rg` over `app/**/*.py` for park/saved-search/search_mem/mnemonic → **no matches** (greenfield confirmed).
- Mount pattern: `app/api/routes/api.py` `include_router` for auth/users/profiles/articles/comments/tags — parks will follow same style.
- Seat gate: `get_current_user_authorizer()` in `app/api/dependencies/authentication.py` (reused on articles/comments/profiles/users).
- Not-found polarity: `EntityDoesNotExist` in `app/db/errors.py`; comments load uses 404 on miss (`dependencies/comments.py`) then **separate** 403 on non-author modify (`check_comment_modification_permissions`) — parks must **not** copy the 403 disclose path; owner-scoped get → 404 only.
- Ownership FK precedent: `favorites.user_id` → `users.id` CASCADE and `commentaries.author_id` in `fdf8821871d7_main_tables.py`; no `parks` table today.
- Wire envelope precedent: Conduit embed schemas under `app/models/schemas/` (e.g. `CommentInCreate` / `CommentInResponse`).
- Harness: `tests/verify/` and `tests/README.md` absent; as-built dir empty — FF-01/FF-02 remain plan/ground work.
- No `scripts/create_postgres_migration.sh` in this repo — Alembic revisions live under `app/db/migrations/versions/` (Wave0a chassis).

**Boundary diagram (text):**

```
HTTP client (Bearer seat)
  → [app/api/routes/parks.py]
       → [app/api/dependencies/parks.py + authentication]
            → [app/db/repositories/parks.py]
                 → [Postgres: parks  owner_id → users.id]
  Unseated / missing bearer → authorizer 401 (no disclosure)
  Missing or non-owned park_id → EntityDoesNotExist → HTTP 404
  Relabel body: label only (query column immutable at write path)
```

**Existing Accepted ADR constraints:**

| ADR | Interaction |
|-----|-------------|
| ADR-001 | **constrains** — package root remains `app/`; no `src/` migrate in this INIT (Q-08 / FF-04) |
| ADR-002 | independent — favorites shelf authorization; do not reopen or share tables |
| ADR-003 | independent — `favoritesCount` wire |
| ADR-004 | **constrains** — unseat = client JWT discard; park rows survive reseat (REQ-08) |
| ADR-005 | independent — subscribe idempotency |
| ADR-006 | independent — Guest `following` omit |

---

## 3. Public interface contracts

### 3.1 Park create → repository

**Method / entry point:** `create_park` (router) → `ParksRepository.create_park`

**Arguments:**
- seated `user` required (`get_current_user_authorizer()`)
- body: query string + optional mnemonic label (Conduit-style embed envelope, e.g. `{ "park": { ... } }`)
- after trim: query must be non-empty; blank/whitespace-only label stored as null

**Return:**
- single park resource: stable integer `id`, retained query text, label or null, park timestamp
- HTTP 201 on success

**Invariants:**
- Empty/whitespace query → refuse create (validation error); owner recall unchanged
- Duplicate query strings / non-unique labels allowed for same owner (no unique constraint)
- Rows keyed by `owner_id`; no peer visibility on create response beyond caller's own row
- Eng ceilings: query ≤ 2048 chars; label ≤ 128 chars; ≤ 200 parks per owner — reject over-limit as validation/terminal without inventing product CAP numbers

### 3.2 Own recall list → repository

**Method / entry point:** `list_own_parks` → `ParksRepository.list_parks_for_owner`

**Arguments:**
- seated `user` required
- no peer-username or foreign-owner filter parameters

**Return:**
- ordered list newest-first by park time (`created_at DESC`, then `id DESC` tie-break)
- empty list valid (HTTP 200)

**Invariants:**
- Result set ⊆ caller's `owner_id` only
- Each item preserves parked query string fidelity

### 3.3 Relabel → repository

**Method / entry point:** `relabel_park` → `ParksRepository.update_park_label`

**Arguments:**
- path `park_id` (int ≥ 1)
- seated owner required
- body: label field only (omit/blank/whitespace → clear to null); **no** query rewrite field on this contract

**Return:**
- updated park resource; query column unchanged

**Invariants:**
- Load path scopes by `(id, owner_id)`; miss → `EntityDoesNotExist` → HTTP 404 (same for peer-owned ids — never 403 that would disclose existence)
- Query column has no update setter in repository API for this INIT

### 3.4 Discard → repository

**Method / entry point:** `discard_park` → `ParksRepository.delete_park_for_owner`

**Arguments:**
- path `park_id`; seated owner required

**Return:**
- HTTP 204; subsequent own recall omits the row
- Empty recall after last discard remains HTTP 200 `[]`

**Invariants:**
- Same owner-scoped not-found polarity as relabel
- Unseated attempts fail at authorizer (401) with no mutation

### 3.5 Seat gate (shared)

**Method / entry point:** `get_current_user_authorizer(required=True)` on all park routes

**Arguments / return:** existing JWT bearer verification

**Invariants:**
- Unseat = omit bearer (ADR-004); park rows remain in Postgres across reseat
- No logout wipe path for parks

---

## 4. ADR resolutions

Feasibility reported **`new_adr: false`** — no `NEW-ADR` / `ALTERNATIVE:` findings. Zero Draft ADR files required. Ordinary engineering choices below are `TDD_ONLY` under Accepted ADR-001 / ADR-004.

| Finding | Classification | ADR file / TDD section | product_constraints | Product exclusions | Recommendation / default | Status | Digest |
|---------|----------------|------------------------|---------------------|--------------------|--------------------------|--------|--------|
| FF-03 / E-01 | TDD_ONLY | §9 E-01; §2–§3 | `[REQ-01..REQ-16]` | favorites/follow reopen | Dedicated `parks` table + `ParksRepository` under `app/` | Resolved | N/A |
| E-02 | TDD_ONLY | §9 E-02; §3 | `[REQ-01..REQ-16]` | web UI / auto-run | Mount `/parks` router; integer path id; Conduit embed envelopes | Resolved | N/A |
| E-03 | TDD_ONLY | §9 E-03 | IM-04 / NFR Performance | product CAP numbers | Eng ceilings 2048 / 128 / 200 | Resolved | N/A |
| E-04 | TDD_ONLY | §9 E-04; §3.3–3.4 | `[REQ-13]` | comments-style 403 disclose | Owner-scoped load → `EntityDoesNotExist` → 404 only | Resolved | N/A |
| Q-08 / FF-04 | TDD_ONLY | §9 Q-08 | chassis | `src/` migrate | Continue Accepted ADR-001 Option A | Resolved | N/A |
| FF-01 | TDD_ONLY | §5 / §12 | live CAP/J | — | Plan creates `tests/verify` + `tests/README.md` | Resolved (plan) | N/A |
| FF-02 | TDD_ONLY | §12 | as-built | — | Seed as-built gap rows at ground / first wave | Resolved (ground) | N/A |

**Derived counts:**

- ADR_REQUIRED: 0
- TDD_ONLY: 7
- DEFERRED_WITH_DEFAULT: 0
- Draft ADR files created: 0
- Missing/broken ADR files: 0

---

## 5. Test policy

| Module / area | Unit layer tests | Integration layer | Live verify | Golden test strategy |
|---------------|-----------------|-------------------|-------------|----------------------|
| Park create | labeled / unlabeled / blank-label→null; empty/whitespace query refuse; eng over-limit refuse; duplicates allowed | TestClient + Postgres `parks` | CAP-01 / J-01, J-02, J-12 | exact status + query/label fields |
| Own recall | ownership filter; newest-first; empty list valid | TestClient + seeded timestamps | CAP-02 / J-03 | exact id order for seeded set |
| Relabel / clear | label change; clear-to-null; query unchanged; no query field accepted | TestClient + DB column assert | CAP-02 / J-04 | exact label + query fidelity |
| Discard | remove one; last discard → empty list | TestClient | CAP-02 / J-05, J-10 | exact membership |
| Isolation | peer list empty of foreign rows; peer mutate 404; unseated 401 | TestClient multi-user | CAP-03 / J-06, J-07, J-09, J-11 | exact status; no query leakage |
| Durability | DB row survives client omit-bearer then reseat JWT; list still returns same `query_text` | TestClient + Postgres across auth sessions | CAP-02 / J-08 | exact query string |
| Harness | N/A | N/A | create `tests/verify/verify_parks.py` (name may vary) + `tests/README.md` | exit 0/nonzero |

**AI-output determinism policy (when applicable):**
- N/A — no LLM outputs in this provider.

**Vocabulary:** unit = handler/repo with doubles or isolated TestClient+DB as today’s `tests/test_*` suite; integration = one real boundary (Postgres) via existing async fixtures — never “whole compose stack”; live verify / smoke = human-run under `tests/verify` against `realworld-local` compose.

---

## 6. Error handling strategy

| Failure mode | Module where it originates | Propagation path | Recovery |
|--------------|---------------------------|------------------|----------|
| Unseated park/list/relabel/discard | auth dependency | HTTP 401 | terminal — no row write/read disclosure |
| Empty/whitespace query on create | parks schema / route validation | HTTP 422 (or baseline validation status) | terminal — no insert |
| Eng ceiling exceeded | schema / service guard | HTTP 422 | terminal |
| Missing park_id | `dependencies/parks.py` | `EntityDoesNotExist` → HTTP 404 | terminal |
| Non-owned park_id | repository owner-scoped get | same 404 path (no 403) | terminal — own recall unchanged |
| Peer list attempt | list query filters `owner_id` | HTTP 200 with peer’s own rows only (never foreign) | N/A |
| Empty own recall | list repo | HTTP 200 `[]` | valid |
| Incomplete create | repository transaction | raise before commit | terminal — no partial visible row |

---

## 7. Observability contract

| Module | Log level | Structured fields | Notes |
|--------|-----------|-------------------|-------|
| Park create | INFO | `owner_id`, `park_id`, `has_label`, `query_len` | Do not log full query text at INFO (privacy) |
| Relabel / discard | INFO | `owner_id`, `park_id`, `action` | |
| List | DEBUG | `owner_id`, `result_count` | |
| Not-found mutate | DEBUG | `actor_id`, `park_id`, `outcome=not_found` | Same log shape for missing vs non-owned |
| Auth deny | existing auth logs | — | unchanged |

Baseline uses `app/core/logging.py`; do not require loguru migrate mid-INIT (ADR-001). Product NFR observability remains N/A as kill criterion.

---

## 8. Data contract ownership

| Schema / data type | Owner (defines + validates) | Validation layer | Versioning |
|--------------------|----------------------------|------------------|------------|
| Park wire create/relabel/list | `app/models/schemas/parks.py` + domain | HTTP edge (Pydantic) | INIT-003 freeze; breaking → INIT revision |
| `parks` table | Alembic revision + `ParksRepository` | repository + DB constraints | additive; FK `owner_id` → `users.id` CASCADE |
| Seat / JWT | existing auth stack | middleware / dependency | ADR-004 unseat semantics unchanged |
| Favorites / followers | out of scope | — | do not share tables or reopen INIT-001/002 |

**Persistence shape (locked for plan):**

| Column | Type / notes |
|--------|----------------|
| `id` | integer PK |
| `owner_id` | FK `users.id` ON DELETE CASCADE, indexed |
| `query_text` | non-null text |
| `label` | nullable text |
| `created_at` | timestamptz — park time for newest-first |
| `updated_at` | timestamptz — touched on relabel |

No unique index on `(owner_id, query_text)` or labels.

---

## 9. Resolved engineering decisions

| Finding ID | Owner | Status | Question | Resolution | Required by | Default if deferred | Evidence / reference |
|------------|-------|--------|----------|------------|-------------|---------------------|----------------------|
| Q-08 / FF-04 | PE | resolved | Chassis `app/` vs `src/` for parks | Continue Accepted ADR-001 Option A; product-spec Q-08 marked resolved | plan | — | ADR-001; AF-4 |
| E-01 / FF-03 | PE | resolved | Persistence encoding | Dedicated `parks` table + `ParksRepository` (not favorites reuse, not in-process memory) | plan | — | F2 gap; `app/db/repositories/` pattern |
| E-02 | PE | resolved | Route / identity encoding | New `app/api/routes/parks.py` mounted at `/parks`; integer `park_id`; Conduit embed envelopes | plan | — | comments id pattern; `api.py` mount style |
| E-03 | PE | resolved | Eng reasonableness limits (IM-04) | query ≤2048; label ≤128; ≤200 parks/owner | plan | — | NFR Performance; not product CAP |
| E-04 | PE | resolved | Missing vs non-owned HTTP polarity | Owner-scoped get → `EntityDoesNotExist` → 404 only (no comments-style 403) | plan | — | REQ-13; contrast `dependencies/comments.py` |
| E-05 | PE | resolved | Park-time ordering source | `ORDER BY created_at DESC, id DESC` | plan | — | REQ-14 |
| E-06 | PE | resolved | Query immutability at write API | Relabel repository/API exposes label only; no query update method this INIT | plan | — | REQ-16 |
| FF-01 | PE | resolved | Live verify harness gap | Plan names `tests/verify` module(s) + `tests/README.md` | plan | — | F3 |
| FF-02 | PE | resolved | As-built absent | Seed gap rows at ground / first wave — not a coding blocker for TDD | ground | — | A-07 |

---

## 10. Routed out — product questions (PM)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| — | — | — | none open — Q-01..Q-07 resolved via Impact-Map defaults into REQ-* | — | — | — | Feasibility PM lane | — |

---

## 11. Routed out — domain clarifications (SME)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| — | — | — | none | — | — | — | Feasibility domain lane empty | — |

---

## 12. Fix disposition

| ID | Status | Item | Target/evidence | Result digest |
|----|--------|------|-----------------|---------------|
| AF-1 | planned-auto-fix | Add `tests/verify` + `tests/README.md` when plan names scripts | FF-01 | N/A |
| AF-2 | planned-auto-fix | Seed as-built index rows as gap | FF-02; `docs/specification/as-built/` | N/A |
| AF-3 | planned-auto-fix | Greenfield parks modules in implementation plan §9 | FF-03; E-01/E-02 | N/A |
| AF-4 | auto-fixed | Mark product-spec Q-08 resolved citing ADR-001 | Spec questions table → resolved | `sha256:37ab4aeedbdb73440a00ea968545b6c15fe5e2fc51727e961844184f9568a1bd` |

---

## 13. Implementation readiness verdict

| Gate | Status |
|------|--------|
| All T1–T12 checks | PASS |
| Engineering decisions resolved | 9 resolved, 0 PE deferred; 0 blocking PM/domain |
| Draft ADR files written | 0 / 0 required (`new_adr: false`) |
| Product-boundary integrity (T12) | PASS — `adr_boundary_lint.py --tdd --require-sources` PASS (2 sources); independent Task cold re-read of §1/§5/§9 PASS |
| PM questions outstanding | 0 |
| Domain questions outstanding | 0 |
| Selected workflow outcome | `pass` — engineering decisions resolved/deferred; no NEW-ADR Draft files required; ready for PE review of TDD; no blocking PM/domain |
| Ready for PE review | YES |
| **Ready for /spec-implementation-plan** | **YES** — `Status: Accepted`; zero ADR_REQUIRED; PE sign-off complete 2026-11-12 |

---

## Check summary

| Check | Status | Notes |
|-------|--------|-------|
| T1 Module boundaries | PASS | Greenfield parks under `app/`; T2 grounding (rg + favorites/comments/auth mounts); continue ADR-001 |
| T2 Interface contracts | PASS | create/list/relabel/discard + seat gate shapes and invariants |
| T3 NEW-ADR dispositions | PASS | Feasibility `new_adr: false` — zero `ALTERNATIVE:` Finding cells; all ordinary choices `TDD_ONLY`; ADR_REQUIRED 0 |
| T4 Test policy | PASS | unit / TestClient+Postgres / live verify vocabulary; CAP/J mapping |
| T5 Error handling | PASS | 401 / 422 / 404 polarity named; no comments-style peer 403 disclose |
| T6 Observability | PASS | structured fields; query text not logged at INFO |
| T7 Data contract ownership | PASS | parks wire + table ownership; favorites OOS |
| T8 Dependency graph | PASS | routes → deps → repo → Postgres; no `src/`; no ADR conflict |
| T9 Engineering questions zero | PASS | Q-08 + E-01..E-06 + FF-01/02 resolved |
| T10 PE review readiness | PASS | Draft TDD path listed; `ready_for_pe_review: true`; `ready_for_plan: false` |
| T11 ADR artifact integrity | PASS | N/A files — zero ADR_REQUIRED; no embedded ADR bodies |
| T12 Product-boundary integrity | PASS | `adr_boundary_lint.py --tdd --require-sources` PASS (2 sources); independent Task subagent cold re-read of §1/§5/§9 → PASS |

---

## Forge / PR instructions

> Persist this TDD locally and publish via `/commit-workspace` (or Gateflow
> ForgeClient) to the **Draft spec PR** branch. Do **not** commit, push, open
> PRs, or apply labels inside this skill. PE reviews on the **same PR**.
> Gate 2 label stays **`spec-pending`** until the implementation plan exists.
> PE accepts architecture by publishing **Accepted** TDD/ADR files — not by
> setting `spec-lgtm` yet. CODEOWNERS may request PE review on `Technical-Review-*`.

```
Branch:   chore/INIT-REALWORLD-003-spec-realworld-api
PR title: "[INIT-REALWORLD-003] Spec — realworld-api"
PR body:  link meta PRD PR; paste §13 Implementation readiness verdict when TDD is ready

Required reviewers (enforced by CODEOWNERS when TDD file is present):
  @drivestream-lab/backend-devs  ← must give explicit Approve, not just silence

Review deadline: 2026-11-19
PE review checklist (PE works through this on the spec PR):
  [ ] T1 Module boundaries — can I draw the box?
  [ ] T2 Interface contracts — are shapes and invariants specified?
  [ ] T3 ADR dispositions — zero NEW-ADR; TDD-only rationales valid
  [ ] T4 Test policy — is determinism policy acceptable?
  [ ] T9 Zero unresolved PE items?
  [ ] T11 ADR artifact integrity — N/A (no Draft ADRs required)
  [ ] T12 Product-boundary integrity — every user-visible statement cites approved REQ-*
  [ ] T12 mechanical: `adr_boundary_lint.py --tdd` with --require-sources
  [ ] T12 manual cold re-read of §1 / §5 / §9

PE action (artifact acceptance — mid-lane):
  Review/comment or Request changes → developer updates TDD files
  Explicitly state when decisions are ready for acceptance
  Developer/PE updates TDD Status → Accepted
  Publish acceptance package via Forge to spec branch (label remains spec-pending)

After artifact acceptance:
  → /spec-implementation-plan may run on the same branch
  → after plan on head: PE sets spec-lgtm + Approve + attestation
  → Ready for review → merge → `/create-board-tickets` from plan §9
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-technical-review
  outcome: pass
  artifact:
    path: docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8
    scope_digest: sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7
    meta_pr_approved_head: abfbbcff877a83c298776fd4801b8ac4c75ddfba
    new_adr: false
    new_adr_ids: []
    draft_adr_paths: []
    ready_for_pe_review: true
    ready_for_plan: true
    codegraph_provider: degraded-none
    grounding_depth: light
    t12_lint: pass
    t12_independent_reread: pass
    outcome_rationale: zero NEW-ADR (no ALTERNATIVE findings); Q-08 + parks persistence/route/limit/isolation resolved as TDD_ONLY under ADR-001/004; T12 lint + independent re-read PASS; Status Accepted — ready for plan
  next_candidates:
    - technical-review-approval
  human_checkpoint: true
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-003] Spec — realworld-api (technical review)"
    body_path: docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md
    target_branch: chore/INIT-REALWORLD-003-spec-realworld-api
```
