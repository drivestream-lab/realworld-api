# Technical Design Document — INIT-REALWORLD-002

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-002 |
| Spec | `docs/specification/product/INIT-REALWORLD-002-api.md` |
| Spec digest | `sha256:b6d9a028486a5f94c6e4f5d42bd539584ed35091d5b71f7f8665f5fb47b79b4a` |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md` |
| PRD digest | `sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-002.md` / `1` |
| Repo scope digest | `sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0` |
| Approved meta PR head | `ee9fe45ad23d988eface7517a3a65a7b58b592c1` |
| Source freshness | CURRENT — H1 live PRD digest matches spec citation; H2 api scope digest matches impact-map row (`capabilities=CAP-01..CAP-04`); H3 `map_revision=1`; G1 APPROVED review `commit_id` equals merged meta PR #8 head; feasibility tip continuous; Hermes re-run refreshed TDD/ADR digests + AF-3/AF-4 |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Branch | `docs/spec-init-realworld-002` (Draft spec PR [#11](https://github.com/drivestream-lab/realworld-api/pull/11) — TDD published via Forge) |
| Initiative segment | `INIT-REALWORLD-002` |
| Status | Accepted |
| Review deadline | 2026-11-19 |
| Deciders | PE: @drivestream-lab/backend-devs — explicit LGTM required, not approval by silence |

---

## 1. Problem statement

Follow/feed providers already live under `app/` (Accepted ADR-001), but two wire forks remain: same-state subscribe returns HTTP 400 today (product-locked to success-no-op), and Guest profile JSON always emits `following: false` even when no edge was loaded. Global listing has no ORDER BY and the subscription-stream SQL sorts `created_at` ascending, so newest-first (REQ-21) drifts. This TDD locks the wire ADRs, ordering columns, module contracts, and test policy so plan TASKs have one target graph.

---

## 2. Module / package boundaries

| Module | Current state | Change | Owns |
|--------|---------------|--------|------|
| `app/api/routes/profiles.py` | exists | extend — same-state subscribe success (ADR-005); keep unsubscribe same-state 400 | HTTP follow/unfollow edge |
| `app/models/domain/profiles.py` + `app/models/schemas/profiles.py` | exists | extend — Guest omit `following` (ADR-006) | Profile wire |
| `app/db/repositories/profiles.py` | exists | unchanged edge CRUD; callers stop raising on same-state | Subscription graph persistence |
| `app/api/routes/articles/articles_resource.py` | exists | unchanged list entry; inherits repo ORDER BY | Public/global listing HTTP |
| `app/db/repositories/articles.py` (`filter_articles`) | exists | extend — newest-first ORDER BY | Global/tag/author listing query |
| `app/db/queries/sql/articles.sql` (`get-articles-for-feed`) | exists | extend — DESC newest-first | Subscription stream SQL |
| `app/api/routes/articles/articles_common.py` | exists | unchanged feed entry after SQL fix | Feed HTTP |
| `tests/test_api/test_routes/test_profiles.py` / `test_articles.py` | exists | invert duplicate-follow + guest-key tests; add stream lifecycle units | In-process proof |
| `tests/verify/` + `tests/README.md` | absent | create in plan (FF-07 / FF-08) | Live smoke + CTR markers |
| `docs/specification/as-built/` | absent | seed at ground / first wave (FF-09) | Maturity index |
| `src/` | absent | **not** introduced (continue ADR-001) | N/A |

**Boundary diagram (text):**

```
HTTP client
  → [app/api/routes/profiles.py | articles_*]
       → [app/db/repositories/profiles.py | articles.py]
            → [Postgres: followers_to_followings / articles]
  Guest profile path: requested_user=None → serialize without following key (ADR-006)
  Same-state subscribe POST: skip write → 200 + following true (ADR-005)
  Same-state unsubscribe DELETE: keep HTTP 400 (TDD §9)
```

**Existing Accepted ADR constraints:**

| ADR | Interaction |
|-----|-------------|
| ADR-001 | **constrains** — package root remains `app/`; no `src/` migrate in this INIT |
| ADR-002 | independent — shelf `favorited=` authorization |
| ADR-003 | independent — `favoritesCount` constant; do not invent follower counts |
| ADR-004 | **constrains** — unseat = client JWT discard; subscription rows survive logout |

---

## 3. Public interface contracts

### 3.1 Profiles follow mutate → repository

**Method / entry point:** `follow_for_user` / `unsubscribe_from_user`

**Arguments:**
- `username` path: target author identity
- seated `user` required (auth dependency)
- repository: `ProfilesRepository.add_user_into_followers` / `remove_user_from_followers`

**Return:**
- `ProfileInResponse` with viewer-relative `following` boolean matching the end-state
- Same-state **subscribe** (already following): HTTP 200, graph unchanged, `following: true` (ADR-005)
- Same-state **unsubscribe** (not following): HTTP 400 `USER_IS_NOT_FOLLOWED` (baseline retained — no approved REQ locks idempotent DELETE)
- Error: self-target → fail-closed 400; missing author → 404 from path dependency; unseated → 401 from authorizer

**Invariants:**
- Directed edge only; no follower/following count fields
- Edges persist across client JWT discard (ADR-004 / REQ-09)

### 3.2 Profiles get → Guest vs seated serialization

**Method / entry point:** `retrieve_profile_by_username` → `get_profile_by_username`

**Arguments:**
- `username` path
- `requested_user`: optional seated caller

**Return:**
- Seated: `following` boolean from edge load
- Guest: JSON **omits** `following` key (ADR-006)
- Error: missing user → 404

**Invariants:**
- Guest omit applies to standalone profile and to author sub-objects when caller is unseated
- Public discovery routes remain optional-auth

### 3.3 Global listing → repository filter

**Method / entry point:** `list_articles` → `ArticlesRepository.filter_articles`

**Arguments:**
- optional `tag` / `author` / `favorited` (favorited still ADR-002-gated)
- `limit` / `offset`
- optional `requested_user`

**Return:**
- article list ordered `updated_at DESC, created_at DESC` (same family as INIT-001 REQ-34 / this INIT REQ-21)
- membership independent of followers join

**Invariants:**
- Guests may list without seat
- Subscription graph changes do not alter membership

### 3.4 Subscription stream → feed SQL

**Method / entry point:** `get_articles_for_user_feed` → `get_articles_for_feed`

**Arguments:**
- seated `user` required
- `limit` / `offset`

**Return:**
- articles whose authors are in `followers_to_followings` for the caller
- ordered `updated_at DESC, created_at DESC` (align SQL with global rule; today ASC on `created_at` only)
- empty list valid (not global fill)

**Invariants:**
- INNER JOIN followers — no silent global fallback
- No peer username parameter — stream private to bearer subject

---

## 4. ADR resolutions

| Finding | Classification | ADR file / TDD section | product_constraints | Product exclusions | Recommendation / default | Status | Digest |
|---------|----------------|------------------------|---------------------|--------------------|--------------------------|--------|--------|
| FF-01 | ADR_REQUIRED | `docs/specification/adr/adr-005-idempotent-subscribe-wire.md` | `[REQ-23, REQ-07]` | Unsubscribe same-state; REQ-10/12 denials | Subscribe same-state → idempotent 200 | Accepted | `sha256:974979cf66e5736bc5abf997913c4d94d2804be6c65e119cb4f7d0475c0c3aae` |
| FF-02 | ADR_REQUIRED | `docs/specification/adr/adr-006-guest-following-field-omit.md` | `[REQ-22, REQ-04]` | Seated boolean REQs | Omit `following` for Guest | Accepted | `sha256:ccda66d6e898245d172b9ef4febd7abb5d99fa2ecff919db22f4c1916de8e3c9` |
| FF-01b | TDD_ONLY | §9 row FF-01b | `[REQ-08]` | — | Unsubscribe same-state keeps Conduit HTTP 400 (no REQ for idempotent DELETE) | Resolved | N/A |
| FF-04 | TDD_ONLY | §9 row FF-04 | `[REQ-21]` | — | `ORDER BY updated_at DESC, created_at DESC` on `filter_articles` | Resolved | N/A |
| FF-05 | TDD_ONLY | §9 row FF-05 | `[REQ-21]` | — | Same ORDER BY family on `get-articles-for-feed` | Resolved | N/A |
| FF-06 | TDD_ONLY | §9 / §5 | `[REQ-16, REQ-17, REQ-18]` | — | Add unfollow/publish-in/delete-out → stream unit cases | Resolved | N/A |
| FF-07 | TDD_ONLY | §5 / §9 | CTR-01..04 | — | Name verify modules under `tests/verify` with `prayog:covers` | Resolved | N/A |
| FF-03 | TDD_ONLY | §9 row FF-03 | chassis | — | Continue Accepted ADR-001; no supersede | Resolved | N/A |
| Q-12 | TDD_ONLY | §9 row Q-12 | chassis | — | Continue ADR-001 Option A (`app/`) | Resolved | N/A |

**Derived counts:**

- ADR_REQUIRED: 2
- TDD_ONLY: 7
- DEFERRED_WITH_DEFAULT: 0 (PE-lane); PM later items listed in §10
- Draft ADR files created: 2
- Missing/broken ADR files: 0

---

## 5. Test policy

| Module / area | Unit layer tests | Integration layer | Live verify | Golden test strategy |
|---------------|-----------------|-------------------|-------------|----------------------|
| Subscribe stewardship | first subscribe/unsubscribe; same-state subscribe 200 (ADR-005); same-state unsubscribe 400 retained; self/missing deny | TestClient + Postgres followers table | CTR-02 / J-04, J-07, J-12, J-13 | exact status + `following` boolean |
| Guest profile wire | Guest response key omit (ADR-006); seated true/false | TestClient optional-auth | CTR-02 / J-09 | exact JSON key presence/absence |
| Global listing order | ≥2 articles → newest-first by updated/created | TestClient + seeded timestamps | CTR-01 / J-03 | exact slug order for seeded set |
| Subscription stream | ⊆ followed authors; empty not global; unfollow removes; publish-in; delete-out; ORDER BY DESC | TestClient + SQL feed | CTR-03 / J-05, J-06, J-08, J-11, J-15, J-16 | exact membership + order |
| Public/tag independence | subscribe churn does not change list/tag membership | TestClient | CTR-01/04 / J-14 | exact membership sets |
| Harness | N/A | N/A | create `tests/verify/verify_*.py` + `tests/README.md` feature map | exit 0/nonzero |

**AI-output determinism policy (when applicable):**
- N/A — no LLM outputs in this provider.

**Vocabulary:** unit = handler/repo with doubles or isolated TestClient+DB as today’s `tests/test_*` suite; integration = one real boundary (Postgres) via existing async fixtures — never “whole compose stack”; live verify / smoke = human-run under `tests/verify` against `realworld-local` compose.

**Named CTR verify placement (FF-07):** plan MUST create modules such as `tests/verify/verify_discovery.py`, `verify_subscriptions.py`, `verify_subscription_stream.py`, `verify_tags_under_churn.py` (exact filenames may vary) with `prayog:covers` markers for CTR-01..04 / CAP-01..04 / J-* cited in the spec. Document commands in `tests/README.md`.

---

## 6. Error handling strategy

| Failure mode | Module where it originates | Propagation path | Recovery |
|--------------|---------------------------|------------------|----------|
| Unseated follow/unfollow | auth dependency | HTTP 401 | terminal — no edge write |
| Self-subscribe / self-unsubscribe | `profiles.py` | HTTP 400 | terminal — graph unchanged |
| Missing author on follow path | `get_profile_by_username_from_path` | HTTP 404 | terminal |
| Same-state subscribe (already following) | `profiles.py` | HTTP 200 (ADR-005) | N/A — idempotent success |
| Same-state unsubscribe (not following) | `profiles.py` | HTTP 400 | terminal — graph unchanged (baseline retained) |
| Empty subscription stream | feed SQL / repo | HTTP 200 `[]` | valid — not an error wall |
| Unseated feed read | feed route authorizer | HTTP 401 | terminal — no public stream reveal |
| Guest profile read | profiles get | HTTP 200 without `following` key | N/A |

---

## 7. Observability contract

| Module | Log level | Structured fields | Notes |
|--------|-----------|-------------------|-------|
| Follow mutate | INFO on edge add/remove; DEBUG on same-state no-op | `actor_username`, `target_username`, `action`, `noop` | Avoid logging as auth failures |
| Feed read | INFO | `actor_username`, `result_count`, `limit`, `offset` | |
| Guest profile | DEBUG | `target_username`, `following_emitted=false` | |
| Listing order | DEBUG optional | `order=updated_at,created_at` | |

Baseline uses `app/core/logging.py`; do not require loguru migrate mid-INIT (ADR-001). Product NFR observability remains N/A as kill criterion.

---

## 8. Data contract ownership

| Schema / data type | Owner (defines + validates) | Validation layer | Versioning |
|--------------------|----------------------------|------------------|------------|
| Profile wire (`following` optional for Guest) | `app/models/domain/profiles.py` + schemas | HTTP edge serialization (ADR-006) | INIT-002 freeze; breaking → INIT revision |
| Follow mutate response | `profiles.py` handlers | HTTP edge | ADR-005 success envelope |
| Article list / feed rows | `articles` schemas + repos | HTTP edge + SQL | newest-first columns locked here |
| `followers_to_followings` | `ProfilesRepository` + SQL | repository | private graph; not a public count DTO |
| CTR-01..04 semantic seams | product spec tables | verify markers in plan | provider=api / consumer=web |

---

## 9. Resolved engineering decisions

| Finding ID | Owner | Status | Question | Resolution | Required by | Default if deferred | Evidence / reference |
|------------|-------|--------|----------|------------|-------------|---------------------|----------------------|
| FF-01 | PE | resolved | Same-state subscribe: 400 vs idempotent 200 | Idempotent 200 on POST; skip write; return `following: true` | plan | — | ADR-005; `follow_for_user` |
| FF-01b | PE | resolved | Same-state unsubscribe HTTP polarity | Keep Conduit HTTP 400 when not following (no approved REQ for DELETE no-op success) | plan | — | `unsubscribe_from_user`; T12 narrow from FF-01 |
| FF-02 | PE | resolved | Guest profile JSON: key absence vs default boolean | Omit key for Guest; seated keep boolean | plan | — | ADR-006; `Profile.following` |
| FF-04 | PE | resolved | Global listing unordered | `ORDER BY updated_at DESC, created_at DESC` in `filter_articles` | plan | — | REQ-21; mirrors INIT-001 FF-10 |
| FF-05 | PE | resolved | Feed ASC on `created_at` | Same DESC pair on `get-articles-for-feed` | plan | — | `articles.sql` |
| FF-06 | PE | resolved | Missing lifecycle unit coverage | Add unfollow→stream, publish-in, delete-out unit cases before/with live J-06/J-11/J-16 | plan | — | F2 partial rows |
| FF-07 | PE | resolved | CTR verify suite location | `tests/verify` modules + `prayog:covers` for CTR-01..04; document in `tests/README.md` | plan | — | Spec CTR table |
| FF-03 | PE | resolved | Chassis/MDC exception continuity | Cite Accepted ADR-001; no INIT-002 `src/` migrate | plan | — | ADR-001 |
| Q-12 | PE | resolved | `app/` vs `src/` for INIT-002 | Continue ADR-001 Option A | plan | — | ADR-001; `app/` tree |

---

## 10. Routed out — product questions (PM)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| Q-06 / IM-06 | PM | open | Last-unsubscribe empty chrome without re-open | no | later | Next open / re-check sufficient | Impact-Map IM-06 | deferred later |
| Q-07 / IM-07 | PM | open | Clarification rounds per CTR vs PR thread | no | later | Per product PR conversation; ≤2 rounds | Impact-Map IM-07 | programme process |
| Q-11 / IM-11 | PM | open | Delete-out same-visit without re-open | no | later | Next open of stream after delete | Impact-Map IM-11; REQ-18 | deferred later |

---

## 11. Routed out — domain clarifications (SME)

| ID | Owner | Status | Question | Blocking | Required by | Default if deferred | Evidence | Resolution reference |
|----|-------|--------|----------|----------|-------------|---------------------|----------|----------------------|
| — | — | — | none | — | — | — | Feasibility domain lane empty | — |

---

## 12. Fix disposition

| ID | Status | Item | Target/evidence | Result digest |
|----|--------|------|-----------------|---------------|
| AF-1 | planned-auto-fix | Add `tests/verify` + `tests/README.md` when plan names scripts | FF-08 | N/A |
| AF-2 | planned-auto-fix | Seed as-built index rows as gap | FF-09; `docs/specification/as-built/` | N/A |
| AF-3 | auto-fixed | Spec README status → Draft PR #11 open (`spec-pending`) | `docs/specification/README.md` Active product specs row | N/A |
| AF-4 | auto-fixed | Mark product-spec Q-12 resolved citing ADR-001 | Spec questions table → resolved | `sha256:b6d9a028486a5f94c6e4f5d42bd539584ed35091d5b71f7f8665f5fb47b79b4a` |
| AF-5 | suggested-fix | After PE Accept, name Chosen wire for REQ-22/23 in CTR-02 row | product spec CTR table | N/A |

---

## 13. Implementation readiness verdict

| Gate | Status |
|------|--------|
| All T1–T12 checks | PASS |
| Engineering decisions resolved | 9 resolved, 0 PE deferred; 3 non-blocking PM later |
| Draft ADR files written | 2 / 2 required |
| Product-boundary integrity (T12) | PASS — mechanical lint PASS; ADR-005 narrowed to POST-only after first independent FAIL; cold smell-test PASS |
| PM questions outstanding | 3 non-blocking (Q-06, Q-07, Q-11) |
| Domain questions outstanding | 0 |
| Selected workflow outcome | `pass` — engineering decisions resolved; Draft ADRs ready for PE acceptance; no blocking PM/domain |
| Ready for PE review | YES |
| **Ready for /spec-implementation-plan** | **YES — TDD Accepted; ADR-005/ADR-006 Accepted with Lint evidence on Draft PR head** |

---

## Check summary

| Check | Status | Notes |
|-------|--------|-------|
| T1 Module boundaries | PASS | `app/**` mapped; grounded; continue ADR-001 |
| T2 Interface contracts | PASS | follow mutate, Guest serialize, list ORDER BY, feed SQL |
| T3 NEW-ADR dispositions | PASS | FF-01→ADR-005 (subscribe only); FF-01b unsubscribe TDD_ONLY; FF-02→ADR-006 |
| T4 Test policy | PASS | unit / TestClient+DB / live verify; CTR module names |
| T5 Error handling | PASS | 401/404/400 vs idempotent 200 named |
| T6 Observability | PASS | structured fields; kill-criterion N/A |
| T7 Data contract ownership | PASS | Profile/article/feed ownership named |
| T8 Dependency graph | PASS | routes → repos → SQL; no new cycles; ADR-001 |
| T9 Engineering questions zero | PASS | all PE-lane items resolved |
| T10 PE review readiness | PASS | `ready_for_pe_review: true`; `ready_for_plan: false` |
| T11 ADR artifact integrity | PASS | two Draft files linked from §4 |
| T12 Product-boundary integrity | PASS | mechanical lint PASS; independent subagent re-read PASS |

### T12 lint evidence (mechanical)

| Artifact | Result |
|----------|--------|
| ADR-005 | `Lint evidence: adr_boundary_lint.py 3/3, PASS, sha256:55832b61f8093c9b9c4d12931fe2c101a54b49b36537ddc70f830582b7bc05ce` |
| ADR-006 | `Lint evidence: adr_boundary_lint.py 3/3, PASS, sha256:f7052fba2b3eae481bc2ac71ac4d258c4afd3a67f3a3c30b2caa460030570bd2` |
| TDD | `--tdd` lint passed (2 sources: all-reqs + feas Spec quotes); free-text §§ scanned |

### T12 independent re-read

1. Hermes re-run: Draft ADR-005 narrowed to POST same-state only (FF-01b keeps unsubscribe 400 as TDD_ONLY).
2. Independent subagent re-read (no drafting context): ADR-005 **PASS**, ADR-006 **PASS** — Context/Recommendation remain HTTP/serialization engineering after mental strip of `REQ-*`; no 6+ word overlap with Spec quotes; one decision each; boundary flags honestly `false`.
3. Overall T12 manual → **PASS**.

### Code grounding

| Finding | Code evidence (extended) |
|---------|--------------------------|
| FF-01 | `follow_for_user` raises `USER_IS_ALREADY_FOLLOWED`; unit asserts 400 on duplicate POST; ADR-005 covers POST only |
| FF-01b | `unsubscribe_from_user` raises `USER_IS_NOT_FOLLOWED`; retained as baseline 400 (TDD_ONLY) |
| FF-02 | `app/models/domain/profiles.py` `following: bool = False`; `ProfilesRepository.get_profile_by_username` skips edge load when `requested_user` is None; guest test asserts `not following` |
| FF-04 | `ArticlesRepository.filter_articles` limit/offset without ORDER BY |
| FF-05 | `articles.sql` `get-articles-for-feed` `ORDER BY a.created_at` (ASC) |
| FF-06 | feed tests cover empty + following-author only — no unfollow/publish/delete→feed |
| Q-12 / FF-03 | no `src/`; Accepted ADR-001 |

---

## Forge / PR instructions

> Persist this TDD locally and publish via `/commit-workspace` (or Gateflow
> ForgeClient) to the **Draft spec PR** branch. Do **not** commit, push, open
> PRs, or apply labels inside this skill. PE reviews on the **same PR**.
> Gate 2 label stays **`spec-pending`** until the implementation plan exists.
> PE accepts architecture by publishing **Accepted** TDD/ADR files — not by
> setting `spec-lgtm` yet.

```
Branch:   docs/spec-init-realworld-002
PR title: "[INIT-REALWORLD-002] Spec — realworld-api"
PR body:  link meta PRD PR #8; paste §13 Implementation readiness verdict when TDD is ready

Required reviewers:
  @drivestream-lab/backend-devs  ← must give explicit Approve, not just silence

Review deadline: 2026-11-19
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-technical-review
  outcome: pass
  artifact:
    path: docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92
    scope_digest: sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0
    meta_pr_approved_head: ee9fe45ad23d988eface7517a3a65a7b58b592c1
    new_adr: true
    new_adr_ids:
      - FF-01
      - FF-02
    draft_adr_paths:
      - docs/specification/adr/adr-005-idempotent-subscribe-wire.md
      - docs/specification/adr/adr-006-guest-following-field-omit.md
    ready_for_pe_review: true
    ready_for_plan: false
    lane_counts:
      pm_blocking_open: 0
      pe_blocking_open: 0
      domain_blocking_open: 0
      auto_fix_open: 2
    draft_adr_digests:
      - sha256:974979cf66e5736bc5abf997913c4d94d2804be6c65e119cb4f7d0475c0c3aae
      - sha256:ccda66d6e898245d172b9ef4febd7abb5d99fa2ecff919db22f4c1916de8e3c9
    lint_evidence:
      - "Lint evidence: adr_boundary_lint.py 3/3, PASS, sha256:55832b61f8093c9b9c4d12931fe2c101a54b49b36537ddc70f830582b7bc05ce"
      - "Lint evidence: adr_boundary_lint.py 3/3, PASS, sha256:f7052fba2b3eae481bc2ac71ac4d258c4afd3a67f3a3c30b2caa460030570bd2"
    draft_spec_pr: https://github.com/drivestream-lab/realworld-api/pull/11
    codegraph_provider: degraded-none
    grounding_depth: deep
    outcome_rationale: T1-T12 PASS; FF-01/FF-02 Draft ADRs written; ordering and test policy resolved in TDD; ready for PE acceptance before plan
  next_candidates:
    - technical-review-approval
  human_checkpoint: true
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-002] Spec — realworld-api (technical review)"
    body_path: docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md
    target_branch: docs/spec-init-realworld-002
```
