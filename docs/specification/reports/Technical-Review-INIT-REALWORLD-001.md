# Technical Design Document — INIT-REALWORLD-001

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-001 |
| Spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Spec digest | `sha256:006eb93a2b6006b9a8c0c54772f85e9c12c4de67dee3210fb3da15760b5ea360` |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md` |
| PRD digest | `sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-001.md` / `1` |
| Repo scope digest | `sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d` |
| Approved meta PR head | `a500df8eeefbea095ecdd65e00edb128416c3cf4` |
| Source freshness | CURRENT — H1 live PRD digest matches spec citation; H2 api scope digest matches impact-map row; H3 `map_revision=1`; G1 APPROVED `commit_id` equals meta PR #5 head |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-11 |
| Branch | `docs/spec-init-realworld-001` (Draft spec PR [#3](https://github.com/drivestream-lab/realworld-api/pull/3) — TDD published via Forge) |
| Initiative segment | `INIT-REALWORLD-001` |
| Status | Accepted |
| Review deadline | 2026-11-18 |
| Deciders | PE: @drivestream-lab/backend-devs — explicit LGTM required, not approval by silence |

---

## 1. Problem statement

The baseline provider is a Conduit-shaped FastAPI tree under `app/` with no `src/` chassis, an unrestricted `favorited=` repository join, live `favoritesCount` emission, and bearer JWTs without a revoke store. Feasibility FF-01..FF-11 leave open the package-root choice, list-filter authorization predicate, count-field mapping policy, unseat token lifecycle, and several schema/repo gaps (register mint, tag update, tag cardinality, own-favorite guard, identity-field lock, feed ORDER BY). This TDD resolves those engineering decisions against code evidence and approved `REQ-*` ids so plan TASKs have one non-conflicting target graph.

---

## 2. Module / package boundaries

| Module | Current state | Change | Owns |
|--------|---------------|--------|------|
| `app/main.py` + `app/api/routes/*` | exists | extend (seat/tag/shelf/nameplate rules); leave OOS mounts mounted but out of Wave0a verify covers | HTTP edge |
| `app/api/dependencies/authentication.py` | exists | unchanged mechanism (bearer → user); register/login issuance policy adjusted | Auth edge |
| `app/services/jwt.py` | exists | unchanged algorithm; no revoke store | Token mint/decode |
| `app/db/repositories/articles.py` | exists | extend: owner-scoped `favorited` filter; tag-set update; ORDER BY; tag cardinality guards at service/route | Article persistence |
| `app/db/repositories/users.py` | exists | extend: reject username/email mutation on self-update path | User persistence |
| `app/models/schemas/articles.py` / `users.py` | exists | extend `ArticleInUpdate.tagList`; tighten create tags default; lock `UserInUpdate` identity fields | Wire schemas |
| `tests/test_*` | exists | invert shelf-filter polarity; add denial/unit cases for FF-05..FF-10 | In-process proof |
| `tests/verify/` + `tests/README.md` | absent | create in plan (AF-1) | Live smoke |
| `docs/specification/as-built/` | absent | seed at ground / first wave (AF-2) | Maturity index |
| `src/` | absent | **not** introduced in Wave0a (ADR-001) | N/A |

**Boundary diagram (text):**

```
HTTP client
  → [app/api/routes/*]  (auth optional/required)
       → [app/services/*]  (jwt, slug helpers)
       → [app/db/repositories/*]
            → [Postgres via asyncpg]
```

---

## 3. Public interface contracts

### 3.1 Articles list → repository filter

**Method / entry point:** `list_articles` → `ArticlesRepository.filter_articles`

**Arguments:**
- `tag` / `author`: optional strings — public bulletin filters (unchanged)
- `favorited`: optional username — **owner-scoped only** (ADR-002)
- `requested_user`: optional seated user from bearer
- `limit` / `offset`: pagination ints

**Return:**
- ordered article list newest-first by `updated_at` then `created_at` (REQ-34)
- Error / denial: when `favorited` is set and caller is missing or username ≠ subject → fail-closed **403** with stable error body (do not return peer shelf rows; do not 200-with-foreign-rows)

**Invariants:**
- Guests may list global/tag/author without seat
- Peer/guest cannot obtain another member’s favorite rows via this filter

### 3.2 Favorite mutate → repository

**Method / entry point:** `mark_article_as_favorite` / `remove_article_from_favorites`

**Arguments:**
- `slug` path article; seated `user` required

**Return:**
- article payload with `favorited` boolean for **caller only**; `favoritesCount` forced to `0` (ADR-003)

**Invariants:**
- Own-article favorite rejected (REQ-28); missing/deleted → not-found (REQ-35)
- No author check exists today — must be added before Wave0a prove

### 3.3 Auth register / login

**Method / entry point:** `register`, `login`

**Arguments:**
- register: unique username + email + password
- login: email + password

**Return:**
- login: `UserWithToken` (seat)
- register: membership confirmation **without** issuing a contribution seat token (FF-05) — response may omit `token` or use a non-seating envelope; kill-path authenticate uses login only

**Invariants:**
- Duplicate identity fail-closed (REQ-09)
- Unseat = client stops sending bearer (ADR-004); no logout RPC

### 3.4 Article create / update tags

**Method / entry point:** `create_new_article`, `update_article_by_slug`

**Arguments:**
- create: title, description, body, `tagList` with ≥1 non-blank tag after trim
- update: optional title/description/body **and** optional `tagList`; if `tagList` present must retain ≥1 non-blank tag

**Return:**
- published article; tag lanes reflect current links

**Invariants:**
- Zero/blank-only tags rejected on create and on tag-set update
- `ArticleInUpdate` today lacks tags — schema + `update_article` must gain tag replace semantics

### 3.5 Nameplate self-update

**Method / entry point:** `update_current_user`

**Arguments:**
- optional `bio` / `image` only for Wave0a self-update

**Return:**
- updated user + refreshed token for seated caller

**Invariants:**
- username/email changes rejected even if present in body (REQ-30)
- peer update has no route (ownership via current-user only)

---

## 4. ADR resolutions

| Finding | Classification | ADR file / TDD section | product_constraints | Product exclusions | Recommendation / default | Status | Digest |
|---------|----------------|------------------------|---------------------|--------------------|--------------------------|--------|--------|
| FF-01 | ADR_REQUIRED | `docs/specification/adr/adr-001-wave0a-package-chassis.md` | `[REQ-01, REQ-08, REQ-10, REQ-12, REQ-15, REQ-20, REQ-25, REQ-27, REQ-30, REQ-34]` | REQ-01..35 product acceptance | Retain/harden `app/` | Accepted | `sha256:e6d7c257914cfc04faffa8d5517ff898b2add45b789bdd71a9872859d1a37233` |
| FF-02 | ADR_REQUIRED | `docs/specification/adr/adr-002-private-shelf-list-authorization.md` | `[REQ-27]` | REQ-25/26 mutations | Owner-only `favorited` filter | Accepted | `sha256:f2e6e48303e5f81e35cc30b5ba5b8c774c3a06370e546e1a066d7f01ec59ed9e` |
| FF-03 | ADR_REQUIRED | `docs/specification/adr/adr-003-favorites-count-wire-policy.md` | `[REQ-25]` | REQ-27 listing | Force `favoritesCount=0` | Accepted | `sha256:b1db40a8d04872a8dc3befbffeff92ed32e57d440f720900611d1bfdc7d601fa` |
| FF-04 | ADR_REQUIRED | `docs/specification/adr/adr-004-wave0a-unseat-token-discard.md` | `[REQ-12, REQ-13]` | Q-05 cascade | Client JWT discard | Accepted | `sha256:0200f2b21331a99f1d4f6009e15bf198cfd6846ff07035499115fd26b8776f50` |
| FF-05 | TDD_ONLY | §9 row FF-05 | `[REQ-08, REQ-10]` | — | Register does not issue seat JWT; login seats | Resolved | N/A |
| FF-06 | TDD_ONLY | §9 row FF-06 | `[REQ-20, REQ-21, REQ-22]` | — | Add `tagList` to update schema/repo | Resolved | N/A |
| FF-07 | TDD_ONLY | §9 row FF-07 | `[REQ-16]` | — | Reject empty/blank-only create tags | Resolved | N/A |
| FF-08 | TDD_ONLY | §9 row FF-08 | `[REQ-28]` | — | Reject favorite when caller is author | Resolved | N/A |
| FF-09 | TDD_ONLY | §9 row FF-09 | `[REQ-30]` | — | Ignore/reject username/email on self-update | Resolved | N/A |
| FF-10 | TDD_ONLY | §9 row FF-10 | `[REQ-34]` | — | ORDER BY updated_at DESC, created_at DESC | Resolved | N/A |
| FF-11 | TDD_ONLY | §9 row FF-11 | same as FF-01 | — | Folded into ADR-001 MDC exception | Resolved | N/A |
| Q-05 | DEFERRED_WITH_DEFAULT | §9 row Q-05 | `[REQ-12]` | — | Unseat logging-out session only | Deferred | N/A |
| Q-09 | DEFERRED_WITH_DEFAULT | §9 row Q-09 | `[REQ-33]` | — | Next navigation / reopen not-found sufficient | Deferred | N/A |

**Derived counts:**

- ADR_REQUIRED: 4
- TDD_ONLY: 7
- DEFERRED_WITH_DEFAULT: 2
- Draft ADR files created: 4
- Missing/broken ADR files: 0

**Existing Accepted ADR constraint table:** `{adr_dir}` empty — no constraining Accepted ADRs (independent).

---

## 5. Test policy

| Module / area | Unit layer tests | Integration layer | Live verify | Golden test strategy |
|---------------|-----------------|-------------------|-------------|----------------------|
| Auth seat | register uniqueness; login success/fail; register response has no seat token; protected routes 401 without bearer | asyncpg + TestClient for register→login→publish | `tests/verify` CAP-02 / J-05..J-08, J-11 | exact status + body keys |
| Articles read | list ordering; tag/author filters; guest access | TestClient against DB fixtures | CAP-01 / J-01..J-04, J-17 | exact order of slugs for seeded set |
| Articles write | zero-tag create/update refuse; ownership deny; tag-set replace | TestClient + DB tag links | CAP-03/04 / J-06, J-09, J-10, J-15 | exact lane membership |
| Private shelf | own-favorite refuse; peer `favorited=` deny; count always 0 | TestClient multi-user | CAP-05 / J-13, J-16 | exact shelf slugs for owner; peer denied |
| Nameplate | identity fields rejected; bio/image applied | TestClient | CAP-06 / J-13, J-19 | exact public profile fields |
| OOS routes | N/A | N/A | **excluded** from Wave0a covers (FF-14) | N/A |

**AI-output determinism policy (when applicable):**
- N/A — no LLM outputs in this provider.

**Vocabulary:** unit = handler/repo with doubles or isolated TestClient+DB as today’s suite; integration = one real boundary (Postgres) via existing async fixtures; live verify = human-run smoke under `tests/verify` against compose (`realworld-local`).

---

## 6. Error handling strategy

| Failure mode | Module where it originates | Propagation path | Recovery |
|--------------|---------------------------|------------------|----------|
| Missing/invalid bearer on contribution | auth dependency | HTTP 401 | terminal for that request |
| Peer shelf list via `favorited` | articles list | HTTP 403 | terminal — no rows |
| Zero/blank tags create/update | articles route validation | HTTP 422/400 | terminal — no write |
| Own-article favorite | favorite handler | HTTP 400/403 (plan picks one; default 400 to match existing favorite errors) | terminal — shelf unchanged |
| Favorite missing article | path dependency | HTTP 404 | terminal |
| Duplicate register identity | auth register | HTTP 400 | terminal |
| Peer article mutate | modification permission dep | HTTP 403 | terminal |
| Identity field on self-update | users update | HTTP 400 | terminal — no identity change |
| JWT still presented after client “logout” | jwt decode | treated as seated until expiry (ADR-004) | N/A — client must drop bearer |

---

## 7. Observability contract

| Module | Log level | Structured fields | Notes |
|--------|-----------|-------------------|-------|
| Auth routes | INFO on seat issue; WARNING on failed login | `username`/`email` hash or id — avoid raw passwords | NFR observability N/A as kill criterion; follow `logging-loguru.mdc` when chassis logging lands |
| Articles mutate | INFO | `slug`, `author_username`, `tag_count` | |
| Favorite mutate | INFO | `slug`, `actor_username`, `action` | Do not log peer shelf subjects on denied list |
| Denied peer shelf | WARNING | `actor`, `requested_subject` | |

Baseline today uses `app/core/logging.py`; Wave0a does not require migrating to loguru mid-kill-path (ADR-001).

---

## 8. Data contract ownership

| Schema / data type | Owner (defines + validates) | Validation layer | Versioning |
|--------------------|----------------------------|------------------|------------|
| Article wire (`tagList`, `favoritesCount`, `favorited`) | `app/models/schemas/articles.py` + route mappers | HTTP edge | Wave0a freeze; breaking → INIT revision |
| User/auth wire | `app/models/schemas/users.py` | HTTP edge | register response seat-less (FF-05) |
| Favorites join rows | `ArticlesRepository` | repository | private; not a public list DTO |
| JWT claims | `app/services/jwt.py` / `JWTUser` | auth dependency | HS256 secret from settings |

---

## 9. Resolved engineering decisions

| Finding ID | Owner | Status | Question | Resolution | Required by | Default if deferred | Evidence / reference |
|------------|-------|--------|----------|------------|-------------|---------------------|----------------------|
| FF-01 | PE | resolved | Chassis `app/` vs `src/` | Retain/harden `app/` package root | plan | — | ADR-001 |
| FF-02 | PE | resolved | Unrestricted vs gated `favorited=` join | Gate join on `requested_user.username == favorited`; else fail-close | plan | — | ADR-002 |
| FF-03 | PE | resolved | Live `favoritesCount` vs constant | Map `favoritesCount=0` on article responses | plan | — | ADR-003 |
| FF-04 | PE | resolved | Client omit bearer vs server revoke | No revoke store/logout RPC; client drops Authorization | plan | — | ADR-004 |
| FF-05 | PE | resolved | Register mints JWT | Stop minting JWT in `register`; mint only in `login` | plan | — | `authentication.py` |
| FF-06 | PE | resolved | Tag-set on update missing | Add `tagList` to `ArticleInUpdate` + repo tag replace | plan | — | schemas/repo gap |
| FF-07 | PE | resolved | Empty create `tagList` allowed | Validate ≥1 non-blank tag on create | plan | — | `ArticleInCreate.tags` |
| FF-08 | PE | resolved | Missing author guard on favorite | Reject when `article.author.username == caller.username` | plan | — | `mark_article_as_favorite` |
| FF-09 | PE | resolved | Identity fields on `UserInUpdate` | Reject/ignore username/email on self-update path | plan | — | `UserInUpdate` |
| FF-10 | PE | resolved | Feed unordered | `ORDER BY updated_at DESC, created_at DESC` in `filter_articles` | plan | — | `filter_articles` |
| FF-11 | PE | resolved | MDC `src/` unmet | Covered by ADR-001 Wave0a layout exception | plan | — | ADR-001 |
| Q-05 | PE | deferred | Multi-session token cascade | Default: invalidate only the client that drops its bearer | later | same | IM-05 |
| Q-09 | PE | deferred | Mid-read refresh after delete | Default: next GET returns not-found; no push channel | later | same | IM-09 |

---

## 10. Routed out — product questions (PM)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| — | — | — | none blocking | — | — | — | Feasibility PM lane empty | Impact-Map IM defaults already locked |

---

## 11. Routed out — domain clarifications (SME)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| — | — | — | none | — | — | — | Feasibility domain lane empty | — |

---

## 12. Fix disposition

| ID | Status | Item | Target/evidence | Result digest |
|----|--------|------|-----------------|---------------|
| AF-1 | planned-auto-fix | Add `tests/verify` + `tests/README.md` feature map | plan names scripts/covers | N/A |
| AF-2 | planned-auto-fix | Seed as-built index rows as gap | `docs/specification/as-built/` at ground / first wave | N/A |
| AF-3 | suggested-fix | Keep Spec-PR-Body helper aligned on Forge publish | `docs/specification/reports/Spec-PR-Body-INIT-REALWORLD-001-realworld-api.md` | N/A |
| AF-4 | planned-auto-fix | Exclude OOS routes from Wave0a verify covers | plan covers markers | N/A |

---

## 13. Implementation readiness verdict

| Gate | Status |
|------|--------|
| All T1–T12 checks | PASS |
| Engineering decisions resolved | 11 resolved, 2 deferred with defaults |
| Draft ADR files written | 4 / 4 required |
| Product-boundary integrity (T12) | PASS (lint+verify; independent re-read FAIL→rewrite ADR-003/004; re-audit PASS) |
| PM questions outstanding | 0 |
| Domain questions outstanding | 0 |
| Selected workflow outcome | `pass` — engineering decisions resolved/deferred; Draft ADRs ready for PE acceptance; no blocking PM/domain |
| Ready for PE review | YES |
| **Ready for /spec-implementation-plan** | **YES — PE accepted via Buzz `accept tdd-adr` (ADRs Status=Accepted)** |

---

## Check summary

| Check | Status | Notes |
|-------|--------|-------|
| T1 Module boundaries | PASS | `app/**` mapped; code-grounded; no `src/` |
| T2 Interface contracts | PASS | list/favorite/auth/tags/nameplate contracts stated |
| T3 NEW-ADR dispositions | PASS | FF-01..04 → ADR_REQUIRED; FF-05..11 TDD_ONLY; Q-05/Q-09 deferred |
| T4 Test policy | PASS | unit / TestClient+DB / live verify vocabulary defined |
| T5 Error handling | PASS | 401/403/404/400 paths named |
| T6 Observability | PASS | structured fields; kill-criterion N/A noted |
| T7 Data contract ownership | PASS | schema owners + Wave0a freeze |
| T8 Dependency graph | PASS | routes → services/repos → DB; ADR-001 avoids circular `src/` import rewrite |
| T9 Engineering questions zero | PASS | all PE-lane items resolved or deferred with defaults |
| T10 PE review readiness | PASS | `ready_for_pe_review: true`; `ready_for_plan: true` (PE Accepted ADRs 2026-11-11) |
| T11 ADR artifact integrity | PASS | four Accepted files linked; Lint evidence refreshed at plan P13 |
| T12 Product-boundary integrity | PASS | mechanical lint+verify PASS on 4 ADRs + TDD; independent re-read FAIL→rewrite ADR-003/004; re-audit PASS |

### T12 lint commands (executed)

ADR lint + TDD lint via `.harness/skills/spec-technical-review/scripts/adr_boundary_lint.py` (see Acceptance / Lint evidence lines populated after run).

### Code grounding

| Finding | Code evidence (extended) |
|---------|--------------------------|
| FF-01 | `app/main.py`, `app/api/routes/api.py`; no `src/`; profile `source_roots: [src/]` |
| FF-02 | `articles_resource.list_articles` + `filter_articles` favorited join; `test_filtering_by_favorited` |
| FF-03 | `Article.favorites_count`; favorite handlers mutate count |
| FF-04 | no logout route; `app/services/jwt.py` mint only |
| FF-05..10 | register token; `ArticleInUpdate` no tags; create tags default `[]`; no own-favorite check; `UserInUpdate` identity fields; filter without ORDER BY |

`codegraph_provider: degraded-none` — grounded via direct `app/` reads.

---

## Forge / PR instructions

> Persist this TDD locally and publish via `/commit-workspace` (or Gateflow
> ForgeClient) to the **Draft spec PR** branch. Do **not** commit, push, open
> PRs, or apply labels inside this skill. PE reviews on the **same PR**.
> Gate 2 label stays **`spec-pending`** until the implementation plan exists.
> PE accepts architecture by publishing **Accepted** TDD/ADR files — not by
> setting `spec-lgtm` yet.

```
Branch:   docs/spec-init-realworld-001
PR title: "[INIT-REALWORLD-001] Spec — realworld-api"
Draft PR: https://github.com/drivestream-lab/realworld-api/pull/3

Required reviewers:
  @drivestream-lab/backend-devs

Review deadline: 2026-11-18
PE review checklist:
  [ ] T1–T12 as in skill template
  [ ] ADR-001..004 Draft → Accepted only when product-boundary flags remain false
  [ ] Then /spec-implementation-plan on same branch
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-technical-review
  outcome: pass
  artifact:
    path: docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4
    scope_digest: sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d
    meta_pr_approved_head: a500df8eeefbea095ecdd65e00edb128416c3cf4
    ready_for_pe_review: true
    ready_for_plan: true
    new_adr: true
    accepted_adr_paths:
      - docs/specification/adr/adr-001-wave0a-package-chassis.md
      - docs/specification/adr/adr-002-private-shelf-list-authorization.md
      - docs/specification/adr/adr-003-favorites-count-wire-policy.md
      - docs/specification/adr/adr-004-wave0a-unseat-token-discard.md
    codegraph_provider: degraded-none
    grounding_depth: deep
    draft_spec_pr: https://github.com/drivestream-lab/realworld-api/pull/3
    outcome_rationale: PE Accepted ADR-001..004 via Buzz accept tdd-adr; ready_for_plan true; Lint evidence refreshed at plan P13
  next_candidates:
    - spec-implementation-plan
  human_checkpoint: false
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-001] Spec — realworld-api (technical review accepted)"
    body_path: docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md
    target_branch: docs/spec-init-realworld-001
```
