# Technical Design Document — INIT-REALWORLD-004

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-004 |
| Spec | `docs/specification/product/INIT-REALWORLD-004-api.md` |
| Spec digest | `sha256:a33f3891abdb9a5f25380469eb13313260b1a64e540b69453d77102a2116b459` |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md` |
| PRD digest | `sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-004.md` / `1` |
| Repo scope digest | `sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5` |
| Approved meta PR head | `02c74d94cf8748c1cd53a268035a8a84433caf94` |
| Source freshness | CURRENT — H1 live PRD digest match; H2 api scope digest match (`sha256:383c6d92…`); H3 `map_revision=1`; G1 APPROVED `commit_id` = meta PR #12 head; feasibility tip continuous (`new_adr: false`, zero `ALTERNATIVE:` Finding cells) |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Branch | `chore/INIT-REALWORLD-004-spec-realworld-api` (Draft spec PR not open yet — TDD published via Forge) |
| Initiative segment | `INIT-REALWORLD-004` |
| Status | Accepted |
| Review deadline | 2026-11-19 |
| Deciders | PE: @drivestream-lab/backend-devs — explicit LGTM required, not approval by silence |
| Codegraph | degraded-none — grounded via direct `app/` reads (profile `source_roots` lists `src/` but Wave0a tree is `app/` per ADR-001) |
| Grounding depth | light |

---

## 1. Problem statement

Under Accepted ADR-001 (`app/`), the checkout has no Alembic table, repository, schemas, or `api.py` mount for owner-scoped `(user_id, tag_name)` stewardship. The engineering gap is to add that persistence + router boundary, gate writes/reads with `get_current_user_authorizer()`, map owner-scoped dissolve misses through `EntityDoesNotExist` → HTTP 404, and keep writes off residual graphs (`followers_to_followings` / `profiles` follow helpers; public `tags` / article-tag joins; author-feed SQL). ADR-004 JWT discard must not introduce a delete path for the new rows. Traceability ids: REQ-01..REQ-22.

---

## 2. Module / package boundaries

| Module | Current state | Change | Owns |
|--------|---------------|--------|------|
| `app/api/routes/followed_tags.py` | new | create — establish / list / dissolve | HTTP stewardship edge |
| `app/api/routes/api.py` | exists | extend — `include_router` for followed-tags | Route mount |
| `app/models/domain/followed_tags.py` | new | create | Domain edge DTO |
| `app/models/schemas/followed_tags.py` | new | create — create/list envelopes | Wire schemas |
| `app/db/repositories/followed_tags.py` | new | create — owner-scoped CRUD + idempotent insert | Persistence |
| `app/db/queries/tables.py` (+ SQL) | exists | extend — `followed_tags` table descriptor / queries | Query builder / SQL |
| `app/db/migrations/versions/*` | exists (`fdf8821871d7` baseline) | new Alembic revision — `followed_tags` table | Schema evolution |
| `app/api/dependencies/authentication.py` | exists | unchanged reuse | Seat gate |
| `app/db/errors.py` (`EntityDoesNotExist`) | exists | unchanged reuse | Indist. not-found polarity |
| `app/api/routes/profiles.py` / `followers_to_followings` | exists | **unchanged** — residual author-follow | Out of INIT-004 write scope |
| `app/api/routes/tags.py` / `tags` / `articles_to_tags` | exists | **unchanged** — public catalog / article tags | Out of INIT-004 write scope |
| `app/db/queries/sql/articles.sql` (feed join) | exists | **unchanged** — no tag-edge composition | Residual INIT-002 feed |
| `tests/test_api/` / `tests/test_db/` | exists | extend — followed-tag unit modules | In-process proof |
| `tests/verify/` + `tests/README.md` | absent | create in plan (FF-01) | Live smoke |
| `docs/specification/as-built/` | absent | seed at ground / first wave (FF-02) | Maturity index |
| `src/` | absent | **not** introduced (continue ADR-001 / Q-11) | N/A |

**Code grounding (T2 — this pass):**
- `rg` over `app/**/*.{py,sql}` for tag-follow / followed_tag / membership→tag → **no matches** (greenfield confirmed; FF-03).
- Mount pattern: `app/api/routes/api.py` `include_router` for auth/users/profiles/articles/comments/tags — followed-tags follow same style.
- Seat gate: `get_current_user_authorizer()` in `app/api/dependencies/authentication.py`.
- Author-follow (do **not** reuse): `profiles.py` POST/DELETE `/{username}/follow` + `followers_to_followings`; unfollow of non-followed raises HTTP 400 — tag dissolve must **not** copy that polarity (use owner-scoped miss → 404 per REQ-10).
- Not-found polarity: `EntityDoesNotExist` in `app/db/errors.py`; `dependencies/comments.py` loads with 404 on miss, then a **separate** 403 on non-author modify — tag dissolve must **not** copy the 403 disclose path; owner-scoped get by tag name → 404 only.
- Public tags: `tags` table is article-linked catalog (`TagsRepository.get_all_tags` / `create_tags_that_dont_exist`); edge store must **not** require an existing `tags` row (REQ-19 corpus-empty).
- Ownership FK precedent: `favorites.user_id` → `users.id` CASCADE in `fdf8821871d7_main_tables.py`; no membership→tag edge table today.
- Feed non-composition: `articles.sql` subscription feed joins `followers_to_followings` only — leave unchanged (REQ-14).
- Harness: `tests/verify/` and `tests/README.md` absent; as-built dir absent — FF-01/FF-02 remain plan/ground work.
- No `src/` tree; keep Wave0a package root at `app/` (ADR-001 / Q-11).

**Boundary diagram (text):**

```
HTTP client (Bearer seat)
  → [app/api/routes/followed_tags.py]
       → [get_current_user_authorizer]
            → [app/db/repositories/followed_tags.py]
                 → [Postgres: followed_tags  user_id → users.id]
  Unseated / missing bearer → authorizer deny (no disclosure)
  Missing or non-owned tag name on dissolve → EntityDoesNotExist → HTTP 404
  Public GET /tags + article tag filter + author-feed SQL → untouched
  No inbound followers-of-tag route
```

**Existing Accepted ADR constraints:**

| ADR | Interaction |
|-----|-------------|
| ADR-001 | **constrains** — package root remains `app/`; no `src/` migrate in this INIT (Q-11) |
| ADR-002 | independent — favorites shelf authorization; do not reopen or share tables |
| ADR-003 | independent — `favoritesCount` wire |
| ADR-004 | **constrains** — unseat = client JWT discard; tag-follow rows survive reseat (REQ-05) |

---

## 3. Public interface contracts

### 3.1 Establish → repository

**Method / entry point:** `follow_tag` (router) → `FollowedTagsRepository.follow_tag`

**Arguments:**
- seated `user` required (`get_current_user_authorizer()`)
- body: Conduit-style embed envelope with tag name string (e.g. `{ "followedTag": { "tag": "..." } }`)
- normalize: trim outer whitespace; refuse empty-after-trim; identity is case-sensitive after trim

**Return:**
- single followed-tag resource: stored tag name string exactly as normalized
- HTTP 200 or 201 on success (plan picks one Conduit-consistent status; both acceptable if idempotent body identical)
- Re-follow of an already-edged name returns success with the same single edge (no second row)

**Invariants:**
- Empty/whitespace name → refuse (validation error); owner list unchanged
- No FK / existence check against public `tags` table — corpus-empty names allowed
- Rows keyed by `(user_id, tag_name)`; UNIQUE constraint enforces at-most-once per owner
- Eng ceilings: tag name ≤ 64 chars after trim; ≤ 100 edges per owner — reject over-limit as validation/terminal without inventing product CAP numbers
- Do not insert into `followers_to_followings` or mutate public catalog

### 3.2 Own outgoing list → repository

**Method / entry point:** `list_followed_tags` → `FollowedTagsRepository.list_for_owner`

**Arguments:**
- seated `user` required
- no peer-username, foreign-owner, or inbound-followers filter parameters

**Return:**
- ordered list of tag name strings, newest-established-first (`created_at DESC`, then `tag_name ASC` tie-break)
- empty list valid (HTTP 200)

**Invariants:**
- Result set ⊆ caller's `user_id` only
- Each name appears at most once; names match stored fidelity after trim

### 3.3 Dissolve → repository

**Method / entry point:** `unfollow_tag` → `FollowedTagsRepository.unfollow_tag_for_owner`

**Arguments:**
- path tag name (URL-decoded, then trim; same identity rules as establish)
- seated owner required

**Return:**
- HTTP 200/204; subsequent own list omits that name
- Empty list after last dissolve remains HTTP 200 `[]`

**Invariants:**
- Load/delete scopes by `(user_id, tag_name)`; miss → `EntityDoesNotExist` → HTTP 404 (same for peer-targeted identities — never 403 / never profiles-style 400 that would distinguish “not following”)
- Unseated attempts fail at authorizer with no mutation

### 3.4 Seat gate (shared)

**Method / entry point:** `get_current_user_authorizer(required=True)` on all followed-tag routes

**Arguments / return:** existing JWT bearer verification

**Invariants:**
- Unseat = omit bearer (ADR-004); followed-tag rows remain in Postgres across reseat
- No logout wipe path for tag-follow edges

### 3.5 Explicit non-surfaces (this INIT)

**Method / entry point:** none — do not add

**Invariants:**
- No inbound “followers of tag X” list/count route
- Do not rewrite `GET /tags`, article tag-filter membership, or author-subscription feed SQL
- Do not mount tag-follow under `profiles` or reuse `ProfilesRepository` follow helpers

---

## 4. ADR resolutions

Feasibility reported **`new_adr: false`** — no `NEW-ADR` / `ALTERNATIVE:` Finding cells. Zero Draft ADR files required. Ordinary engineering choices below are `TDD_ONLY` under Accepted ADR-001 / ADR-004 (light confirmation of clean feasibility).

| Finding | Classification | ADR file / TDD section | product_constraints | Product exclusions | Recommendation / default | Status | Digest |
|---------|----------------|------------------------|---------------------|--------------------|--------------------------|--------|--------|
| FF-03 / E-01 | TDD_ONLY | §9 E-01; §2–§3 | `[REQ-01..REQ-22]` | author-follow / favorites reopen | Dedicated `followed_tags` table + `FollowedTagsRepository` under `app/` | Resolved | N/A |
| E-02 | TDD_ONLY | §9 E-02; §3 | `[REQ-01..REQ-22]` | web UI / inbound reverse-index | Mount `/followed-tags`; tag-name path identity; Conduit embed envelopes | Resolved | N/A |
| E-03 | TDD_ONLY | §9 E-03 | IM-04 / NFR Performance | product CAP numbers | Eng ceilings tag ≤64 chars; ≤100 edges/owner | Resolved | N/A |
| E-04 | TDD_ONLY | §9 E-04; §3.3 | `[REQ-10]` | profiles 400 / comments 403 disclose | Owner-scoped load → `EntityDoesNotExist` → 404 only | Resolved | N/A |
| E-05 | TDD_ONLY | §9 E-05 | `[REQ-19]` | public `tags` FK | Store `tag_name` text without requiring `tags` row | Resolved | N/A |
| E-06 | TDD_ONLY | §9 E-06 | `[REQ-21]` | — | `ORDER BY created_at DESC, tag_name ASC` | Resolved | N/A |
| Q-11 | TDD_ONLY | §9 Q-11 | chassis | `src/` migrate | Keep package root at `app/` (ADR-001) | Resolved | N/A |
| FF-01 | TDD_ONLY | §5 / §12 | live CAP/J | — | Plan creates `tests/verify` + `tests/README.md` | Resolved (plan) | N/A |
| FF-02 | TDD_ONLY | §12 | as-built | — | Seed as-built gap rows at ground / first wave | Resolved (ground) | N/A |

**Derived counts:**

- ADR_REQUIRED: 0
- TDD_ONLY: 9
- DEFERRED_WITH_DEFAULT: 0
- Draft ADR files created: 0
- Missing/broken ADR files: 0

---

## 5. Test policy

| Module / area | Unit layer tests | Integration layer | Live verify | Golden test strategy |
|---------------|-----------------|-------------------|-------------|----------------------|
| Establish | trim/case identity; empty/whitespace refuse; corpus-empty name allowed; idempotent re-follow; eng over-limit refuse | TestClient + Postgres `followed_tags` | CAP-01 / J-01, J-02, J-11, J-13 | exact status + tag name fields |
| Own list | ownership filter; newest-first; empty list valid; name fidelity | TestClient + seeded timestamps | CAP-02 / J-03 | exact name order for seeded set |
| Dissolve | remove one; last dissolve → empty list; missing → 404 | TestClient | CAP-02 / J-04, J-10, J-12 | exact membership + status |
| Isolation | peer list empty of foreign rows; peer dissolve 404; unseated auth deny; no inbound route | TestClient multi-user | CAP-03 / J-06, J-07, J-09, J-18 | exact status; no name leakage |
| Durability | DB row survives client omit-bearer then reseat JWT | TestClient + Postgres across auth sessions | CAP-02 / J-08 | exact tag name |
| Non-composition | public tag lane / feed unchanged after establish | TestClient against `GET /tags` + feed endpoints | CAP-03 / J-05, J-14, J-16 | exact membership vs pre-follow baseline |
| Concurrent same-tag | two owners independent; one dissolve leaves other | TestClient multi-user | CAP-03 / J-17 | exact per-owner lists |
| Harness | N/A | N/A | create `tests/verify/verify_followed_tags.py` (name may vary) + `tests/README.md` | exit 0/nonzero |

**AI-output determinism policy (when applicable):**
- N/A — no LLM outputs in this provider.

**Vocabulary:** unit = handler/repo with doubles or isolated TestClient+DB as today’s `tests/test_*` suite; integration = one real boundary (Postgres) via existing async fixtures — never “whole compose stack”; live verify / smoke = human-run under `tests/verify` against `realworld-local` compose.

---

## 6. Error handling strategy

| Failure mode | Module where it originates | Propagation path | Recovery |
|--------------|---------------------------|------------------|----------|
| Unseated follow/list/unfollow | auth dependency | HTTP 401 (or baseline auth deny status) | terminal — no row write/read disclosure |
| Empty/whitespace tag on establish | followed-tags schema / route validation | HTTP 422 (or baseline validation status) | terminal — no insert |
| Eng ceiling exceeded | schema / repository guard | HTTP 422 | terminal |
| Missing tag name on dissolve | repository owner-scoped get/delete | `EntityDoesNotExist` → HTTP 404 | terminal |
| Non-owned / peer dissolve attempt | repository owner-scoped get | same 404 path (no 403 / no profiles 400) | terminal — own list unchanged |
| Idempotent re-follow | repository UNIQUE upsert / exists-then-return | HTTP success; single row | N/A |
| Peer list attempt | list query filters `user_id` | HTTP 200 with peer’s own rows only (never foreign) | N/A |
| Empty own list | list repo | HTTP 200 `[]` | valid |
| Incomplete establish | repository transaction | raise before commit | terminal — no partial visible row |

---

## 7. Observability contract

| Module | Log level | Structured fields | Notes |
|--------|-----------|-------------------|-------|
| Establish | INFO | `owner_id`, `tag_len`, `idempotent` | Prefer not logging full tag string at INFO when privacy-sensitive; DEBUG may include normalized name |
| Dissolve | INFO | `owner_id`, `tag_len`, `outcome` | |
| List | DEBUG | `owner_id`, `result_count` | |
| Not-found dissolve | DEBUG | `actor_id`, `tag_len`, `outcome=not_found` | Same log shape for missing vs non-owned |
| Auth deny | existing auth logs | — | unchanged |

Baseline uses `app/core/logging.py`; do not require loguru migrate mid-INIT (ADR-001). Product NFR observability remains N/A as kill criterion.

---

## 8. Data contract ownership

| Schema / data type | Owner (defines + validates) | Validation layer | Versioning |
|--------------------|----------------------------|------------------|------------|
| Followed-tag wire create/list | `app/models/schemas/followed_tags.py` + domain | HTTP edge (Pydantic) | INIT-004 freeze; breaking → INIT revision |
| `followed_tags` table | Alembic revision + `FollowedTagsRepository` | repository + DB constraints | additive; FK `user_id` → `users.id` CASCADE; UNIQUE `(user_id, tag_name)`; **no** FK to `tags` |
| Seat / JWT | existing auth stack | middleware / dependency | ADR-004 unseat semantics unchanged |
| Author-follow / favorites / public tags | out of scope | — | do not share tables or reopen INIT-001/002 |

**Persistence shape (locked for plan):**

| Column | Type / notes |
|--------|----------------|
| `user_id` | FK `users.id` ON DELETE CASCADE, part of PK / unique |
| `tag_name` | non-null text — trimmed, case-sensitive; part of PK / unique |
| `created_at` | timestamptz — establish time for newest-first |

Composite primary key `(user_id, tag_name)` (or UNIQUE equivalent). No surrogate id required. No FK to public `tags`.

**Route mount (locked for plan):**

| Method | Path | Notes |
|--------|------|-------|
| POST | `/followed-tags` | establish; body embed |
| GET | `/followed-tags` | own list |
| DELETE | `/followed-tags/{tag}` | dissolve by URL-decoded tag name |

Mount via `api.py` `include_router(..., prefix="/followed-tags")`. Do not nest under `profiles` or public `/tags`.

---

## 9. Resolved engineering decisions

| Finding ID | Owner | Status | Question | Resolution | Required by | Default if deferred | Evidence / reference |
|------------|-------|--------|----------|------------|-------------|---------------------|----------------------|
| Q-11 | PE | resolved | Chassis `app/` vs `src/` for tag-follow | Keep package root at `app/` per ADR-001; no mid-INIT migrate | plan | — | ADR-001; feasibility Q-11 lock |
| E-01 / FF-03 | PE | resolved | Persistence encoding | Dedicated `followed_tags` table + `FollowedTagsRepository` (not `followers_to_followings`, not in-process memory) | plan | — | F2 gap; `app/db/repositories/` pattern |
| E-02 | PE | resolved | Route / identity encoding | New `app/api/routes/followed_tags.py` at `/followed-tags`; tag-name path; Conduit embed envelopes | plan | — | parks/api.py mount style; profiles path pattern for string identity |
| E-03 | PE | resolved | Eng reasonableness limits (IM-04) | tag ≤64 chars after trim; ≤100 edges/owner | plan | — | NFR Performance; not product CAP |
| E-04 | PE | resolved | Missing vs non-owned HTTP polarity | Owner-scoped get → `EntityDoesNotExist` → 404 only (no profiles 400 / comments 403) | plan | — | REQ-10; contrast `profiles.py` / `dependencies/comments.py` |
| E-05 | PE | resolved | Corpus-empty persistence | Store `tag_name` without requiring public `tags` row | plan | — | REQ-19; `TagsRepository` is catalog-only |
| E-06 | PE | resolved | List ordering source | `ORDER BY created_at DESC, tag_name ASC` | plan | — | REQ-21 |
| E-07 | PE | resolved | Idempotent re-follow encoding | UNIQUE `(user_id, tag_name)` + exists-then-return / upsert; no conflict status required | plan | — | REQ-20 |
| FF-01 | PE | resolved | Live verify harness gap | Plan names `tests/verify` module(s) + `tests/README.md` | plan | — | F3 |
| FF-02 | PE | resolved | As-built absent | Seed gap rows at ground / first wave — not a coding blocker for TDD | ground | — | A-10 |

---

## 10. Routed out — product questions (PM)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| Q-07 / IM-07 | PM | open | Viewer-relative following CTA on public tags? | no | later | No — private outgoing surface enough | Impact-Map IM-07 | Out of scope |
| Q-08 / IM-08 | PM | open | History of former follows after dissolve? | no | later | Fully removed; no history surface | Impact-Map IM-08 | Out of scope |
| Q-09 / IM-09 | PM | open | Favorites vs tag-follow mutual invisibility? | no | later | Separate surfaces; no cross-write | Impact-Map IM-09 | Out of scope |
| Q-10 / IM-10 | PM | open | Future reverse-index without new INIT? | no | later | No — later INIT required | Impact-Map IM-10; REQ-18 | Out of scope |

Material IM-01..IM-06 defaults already locked into REQ-10/19/20/21/22 and NFR Performance — not re-opened here.

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
| AF-3 | planned-auto-fix | Greenfield followed-tags modules in implementation plan §9 | FF-03; E-01/E-02 | N/A |

---

## 13. Implementation readiness verdict

| Gate | Status |
|------|--------|
| All T1–T12 checks | PASS |
| Engineering decisions resolved | 10 resolved, 0 PE deferred; 0 blocking PM/domain |
| Draft ADR files written | 0 / 0 required (`new_adr: false`) |
| Product-boundary integrity (T12) | PASS — `adr_boundary_lint.py --tdd --require-sources` PASS (`sources_checked=2`); independent Task cold re-read of §1/§5/§9 PASS |
| PM questions outstanding | 4 non-blocking (Q-07..Q-10 later) |
| Domain questions outstanding | 0 |
| Selected workflow outcome | `pass` — engineering decisions resolved; no NEW-ADR Draft files required; ready for PE review |
| Ready for PE review | YES |
| **Ready for /spec-implementation-plan** | **NO — final exact-head PE acceptance of this Draft TDD required** |

---

## Check summary

| Check | Status | Notes |
|-------|--------|-------|
| T1 Module boundaries | PASS | Greenfield followed-tags under `app/`; T2 grounding (rg + auth/profiles/tags/favorites mounts); continue ADR-001 |
| T2 Interface contracts | PASS | establish/list/dissolve + seat gate + explicit non-surfaces |
| T3 NEW-ADR dispositions | PASS | Feasibility `new_adr: false` — zero `ALTERNATIVE:` Finding cells; all ordinary choices `TDD_ONLY`; ADR_REQUIRED 0 |
| T4 Test policy | PASS | unit / TestClient+Postgres / live verify vocabulary; CAP/J mapping |
| T5 Error handling | PASS | auth deny / 422 / 404 polarity named; no profiles 400 / comments 403 disclose |
| T6 Observability | PASS | structured fields; tag string privacy noted |
| T7 Data contract ownership | PASS | followed-tags wire + table ownership; author-follow/favorites OOS; no `tags` FK |
| T8 Dependency graph | PASS | routes → auth → repo → Postgres; no `src/`; no ADR conflict; residuals untouched |
| T9 Engineering questions zero | PASS | Q-11 + E-01..E-07 + FF-01/02 resolved |
| T10 PE review readiness | PASS | Draft TDD; `ready_for_pe_review: true`; `ready_for_plan: false` |
| T11 ADR artifact integrity | PASS | N/A files — zero ADR_REQUIRED; no embedded ADR bodies |
| T12 Product-boundary integrity | PASS | `adr_boundary_lint.py --tdd --require-sources` → PASS (`sources_checked=2`); independent Task cold re-read of §1/§5/§9 → PASS |

---

## Forge / PR instructions

> Persist this TDD locally and publish via `/commit-workspace` (or Gateflow
> ForgeClient) to the **Draft spec PR** branch. Do **not** commit, push, open
> PRs, or apply labels inside this skill. PE reviews on the **same PR**.
> Gate 2 label stays **`spec-pending`** until the implementation plan exists.
> PE accepts architecture by publishing **Accepted** TDD/ADR files — not by
> setting `spec-lgtm` yet. CODEOWNERS may request PE review on `Technical-Review-*`.

```
Branch:   chore/INIT-REALWORLD-004-spec-realworld-api
PR title: "[INIT-REALWORLD-004] Spec — realworld-api"
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
    path: docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3
    scope_digest: sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5
    meta_pr_approved_head: 02c74d94cf8748c1cd53a268035a8a84433caf94
    new_adr: false
    new_adr_ids: []
    draft_adr_paths: []
    ready_for_pe_review: true
    ready_for_plan: false
    codegraph_provider: degraded-none
    grounding_depth: light
    t12_lint: pass
    t12_independent_reread: pass
    draft_spec_pr: none
    proposed_branch: chore/INIT-REALWORLD-004-spec-realworld-api
    outcome_rationale: zero NEW-ADR (no ALTERNATIVE findings); Q-11 + followed-tags persistence/route/limit/isolation/corpus-empty resolved as TDD_ONLY under ADR-001/004; T12 lint + independent re-read PASS; ready for PE review — plan blocked until Draft→Accepted
  next_candidates:
    - technical-review-approval
  human_checkpoint: true
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-004] Spec — realworld-api (technical review)"
    body_path: docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md
    target_branch: chore/INIT-REALWORLD-004-spec-realworld-api
```
