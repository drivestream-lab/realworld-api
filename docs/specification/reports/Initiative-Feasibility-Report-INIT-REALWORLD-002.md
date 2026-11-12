# Feasibility report — INIT-REALWORLD-002

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-002 |
| Spec | `docs/specification/product/INIT-REALWORLD-002-api.md` |
| PRD digest | `sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-002.md` / `1` |
| Repo scope digest | `sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0` |
| Approved meta PR head | `ee9fe45ad23d988eface7517a3a65a7b58b592c1` |
| Impact-map approval | Review `PRR_kwDOVac9Rs8AAAABXAtAcQ` / id `5839208561` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T08:58:03Z`; `commit_id` = `ee9fe45ad23d988eface7517a3a65a7b58b592c1` (meta PR [#8](https://github.com/drivestream-lab/realworld-meta/pull/8) MERGED; label `impact-map-lgtm`) |
| Source freshness | CURRENT — H1 live PRD digest matches spec citation; H2 api scope digest recomputed match (`capabilities=CAP-01..CAP-04`); H3 `map_revision=1`; G1 APPROVED review `commit_id` equals merged meta PR #8 head; ripple `continue` |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Branch | `docs/spec-init-realworld-002` — Draft spec PR [#11](https://github.com/drivestream-lab/realworld-api/pull/11) (`spec-pending`) |
| Initiative segment | `INIT-REALWORLD-002` |
| Status | Draft |
| Review deadline | 2026-11-17 |
| Deciders | PM: programme PM · Domain SME: @drivestream-lab/backend-devs |
| Re-run note | Hermes non-interactive re-verification of F1–F14 against live PRD/map/G1 and `app/` evidence; Accepted ADR-001..004 from INIT-001 remain SSOT for chassis / shelf / favoritesCount / unseat |

## Summary

The Wave0a follow/feed baseline under `app/` already covers most CAP-02..CAP-04 provider seams (subscribe/unsubscribe, self/missing denials, empty stream, stream ⊆ followed authors, seat-gated feed), so INIT-REALWORLD-002 is **buildable** without a greenfield chassis move. Source freshness is **CURRENT**. Blocking PE items remain: two **NEW-ADR** wire alternatives (idempotent subscribe vs Conduit 400; Guest `following` omit vs `false`) plus newest-first ordering drifts on global listing and subscription stream. Proceed to `/spec-technical-review` (outcome `findings`); do not set `spec-lgtm`.

**Findings:** 10 total (0 Critical, 6 Should fix, 4 Verify / Gap)

### Derived counts (lane × severity)

| Lane | Blocking open | Non-blocking open | Resolved |
|------|---------------|-------------------|----------|
| PM | 0 | 3 (Q-06, Q-07, Q-11 deferred later) | 8 (Q-01..Q-05, Q-08..Q-10) |
| PE / ADR | 6 | 0 | 1 (Q-12 chassis → cite Accepted ADR-001 continue `app/`) |
| Domain | 0 | 0 | 0 |
| Auto-fix | 0 | 4 | 0 |

| Severity | Unresolved count |
|----------|------------------|
| Critical | 0 |
| Should fix | 6 |
| Verify / Gap (informational) | 4 |

### Selected workflow outcome

| Field | Value |
|-------|-------|
| Outcome | `findings` |
| Rationale | Unresolved blocking PE/ADR items (Should-fix PE-lane) including NEW-ADR wire alternatives and REQ-21 ordering drifts |
| Next (from workflow) | `spec-technical-review` |

Informational observations alone do **not** select `findings`. Unresolved
blocking PE/ADR → `findings`; blocking PM/domain → `needs-input`.

## Baseline snapshot (F1)

| Area | Current state | Evidence |
|------|---------------|----------|
| Unit / in-process tests | Present under `tests/test_api/`, `tests/test_services/`, `tests/test_schemas/`, `tests/test_db/` (not `tests/unit/`). Follow + feed covered in `test_profiles.py` / `test_articles.py`. | `tests/test_api/test_routes/test_profiles.py`, `test_articles.py` (`test_empty_feed_if_user_has_not_followings`, `test_user_will_receive_only_following_articles`); `pyproject.toml` |
| Live verify | **Absent** as SDD `tests/verify/` + `tests/README.md`. Makefile `verify` is a single host curl to `localhost:3100/api/articles`. | `Makefile` `verify` target; no `tests/verify/`; no `tests/README.md` |
| As-built | **Absent** — `docs/specification/as-built/` empty | Spec A-08; empty `docs/specification/as-built/` |
| Source layout | Legacy Conduit package under `app/` (profiles follow, `/articles/feed`, articles list/tags). **No** `src/` tree. Covered by Accepted ADR-001 Option A (retain `app/` for Wave0a; defer platform migrate). | `app/api/routes/profiles.py`, `app/api/routes/articles/articles_common.py`, `app/main.py`; ADR-001 |
| Toolchain | Poetry; black; pytest; Makefile `verify` only (no `make check` / pyright / import-linter yet) | `pyproject.toml`, `Makefile` |
| ADRs | ADR-001..004 **Accepted** (INIT-001). No INIT-002 ADRs yet. | `docs/specification/adr/adr-001-*.md` … `adr-004-*.md` (Status: Accepted) |

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | Package chassis / `app/` vs `src/` | Accepted — continue for INIT-002 unless superseded (resolves spec Q-12 default) |
| ADR-002 | Private-shelf `favorited=` authorization | Accepted — INIT-001 shelf; out of INIT-002 CAP scope |
| ADR-003 | Public `favoritesCount` wire policy | Accepted — INIT-001; counts/social-proof non-goal here |
| ADR-004 | Unseat via client JWT discard | Accepted — supports REQ-09 persistence (logout drops seat, not subscription edges) |

Accepted ADR constraint set for F13: **ADR-001..004**. NEW-ADR candidates are INIT-002 subscription wire semantics only.

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout, JWT verify, `src/` packages, service naming | read — chassis exception via ADR-001 |
| `dependency-injection.mdc` | injector lifecycle | skim — chassis-tied |
| `infra-services.mdc` | DB / outbound clients | skim |
| `repository-pattern.mdc` | repo ↔ ORM boundary | skim |
| `pydantic-schemas.mdc` | models in `src/models/` | read — baseline uses `app/models` under ADR-001 |
| `http-api-conventions.mdc` | body vs query | skim |
| `fail-fast.mdc` | no silent fallbacks | read — empty-stream / denial honesty |
| `testing-verify-flows.mdc` | verify / pytest split | read — F3 harness gap |
| `python-tooling.mdc` | make check / pyright | skim |
| `database-migrations.mdc` | Alembic scripts | skim — followers table exists |
| `strong-typing.mdc` | typing boundaries | skim |
| `python-imports.mdc` | import policy | skipped — N/A to product seams |
| `logging-loguru.mdc` | structured logging | skipped — NFR observability N/A as kill criterion |
| `spec-driven-development.mdc` | SDD discipline | skim |
| `code-guidelines-index.mdc` | index | skim |

## Traceability matrix

| Spec REQ / wave | Spec claim | Code evidence | Unit | Verify | Status |
|-----------------|------------|---------------|------|--------|--------|
| REQ-01 / CAP-01 | Guest public listing ungated | `articles_resource.py` `list_articles` + `get_current_user_authorizer(required=False)` | partial | planned | partial |
| REQ-02 / CAP-01 | Guest open published article | `retrieve_article_by_slug` (no required auth) | partial | planned | partial |
| REQ-03 / CAP-01 | Public tags / empty unknown lane | `tags.py` `get_all_tags`; `list_articles` `tag=` filter | partial (`test_tags.py`) | planned | partial |
| REQ-04 / CAP-01 | Subscribe CTA must not gate reads | Reads remain optional-auth; follow is separate POST | gap (no CTA surface in API) | planned | exists (API) |
| REQ-05 / CAP-01 | Public membership independent of subscriptions | `filter_articles` does not join followers | gap | planned | exists |
| REQ-06 / CAP-01 | Seated global listing subscription-independent | Same `list_articles` path with optional user | partial | planned | exists |
| REQ-07 / CAP-02 | Subscribe → following true | `profiles.py` `follow_for_user` + `ProfilesRepository.add_user_into_followers` | exists (`test_user_can_change_following_for_another_user`) | planned | exists |
| REQ-08 / CAP-02 | Unsubscribe → following false | `unsubscribe_from_user` + `remove_user_from_followers` | exists | planned | exists |
| REQ-09 / CAP-02 | Persist edges across unseat/reseat | `followers_to_followings` table; unseat = client JWT discard (ADR-004) | gap (no logout/reseat integration test) | planned | partial |
| REQ-10 / CAP-03 | Refuse self-subscribe | `follow_for_user` username equality → 400 | exists (`test_user_can_not_change_following_state_for_him_self`) | planned | exists |
| REQ-11 / CAP-03 | Deny unseated mutate | Follow routes use `get_current_user_authorizer()` required | exists (unauthorized parametrized) | planned | exists |
| REQ-12 / CAP-03 | Missing author fail-closed | `get_profile_by_username_from_path` → 404 `EntityDoesNotExist` | partial | planned | exists |
| REQ-13 / CAP-03 | Empty stream valid, not global fill | `get_articles_for_user_feed` + empty-followings test returns `[]` | exists (`test_empty_feed_if_user_has_not_followings`) | planned | exists |
| REQ-14 / CAP-03 | Guest discovery after unseat | Reads optional-auth; mutations still auth-required | gap | planned | partial |
| REQ-15 / CAP-04 | Stream ⊆ subscribed authors | `get_articles_for_feed` INNER JOIN followers | exists (`test_user_will_receive_only_following_articles`) | planned | exists |
| REQ-16 / CAP-04 | Unsubscribe removes from stream | Edge delete + feed join | gap (no explicit unsubscribe→feed unit) | planned | partial |
| REQ-17 / CAP-04 | Publish-in on re-open | Feed joins current followers + articles | gap | planned | partial |
| REQ-18 / CAP-04 | Delete-out on re-open | Deleted article row gone from feed query | gap | planned | partial |
| REQ-19 / CAP-04 | Stream private to subscriber | `/articles/feed` requires auth; no peer username param | partial | planned | exists |
| REQ-20 / CAP-04 | Tag lanes stay tag-true | Tag filter independent of followers | gap | planned | exists |
| REQ-21 / CAP-01/04 | Newest-first global + stream | `filter_articles` **no ORDER BY**; feed SQL `ORDER BY a.created_at` (**ASC**, not DESC) | gap / drift | planned | **drift** |
| REQ-22 / CAP-02/03 | Omit seated subscription state for Guest | `Profile.following: bool = False` always emitted; Guest path never loads edge but still serializes `following: false` | exists (`test_unregistered_user_will_receive_profile_without_following` asserts `not following`) | planned | **drift** vs omit |
| REQ-23 / CAP-02 | Already-subscribed subscribe → stay subscribed, no distinct error | `follow_for_user` raises 400 when `profile.following` already true | exists (`test_user_can_not_change_following_state_to_the_same_twice` expects 400) | planned | **drift** |
| CTR-01..04 | Cross-service seams | Spec table; no consumer contract suite in-repo yet | N/A | planned | planned |
| OOS comments | Non-goal residual | `app/api/routes/comments.py` | exists (OOS) | N/A | residual |

## ADR traceability (F13)

| Spec REQ / wave | Relevant ADR(s) | Status | Code evidence | Finding |
|-----------------|-----------------|--------|----------------|---------|
| CAP-02..04 / Q-12 chassis | ADR-001 | aligned | `app/main.py`, `app/api/routes/profiles.py`, `app/api/routes/articles/articles_common.py` | N/A — continue Accepted Option A (`app/`); supersede only if INIT-002 migrates to `src/` |
| REQ-09 / unseat | ADR-004 | aligned | no logout route; JWT via `app/services/jwt.py`; edges in `followers_to_followings` | N/A — client discard unseats without wiping subscription graph |
| REQ-23 / CTR-02 | NEW-ADR | missing ADR | `app/api/routes/profiles.py` `follow_for_user` / `unsubscribe_from_user` (400 on same-state) | `ALTERNATIVE: keep Conduit HTTP 400 on duplicate subscribe/unsubscribe state vs return idempotent success leaving graph unchanged per REQ-23 wire semantics` |
| REQ-22 / CTR-02 | NEW-ADR | missing ADR | `app/models/domain/profiles.py` `following: bool = False`; `get_profile_by_username` skips edge load when `requested_user` is None | `ALTERNATIVE: omit the following field on Guest profile responses vs emit following false as Conduit default for seated-only subscription state` |
| REQ-21 ordering | N/A (product-locked newest-first; timestamp source eng) | missing implementation | `app/db/repositories/articles.py` `filter_articles`; `app/db/queries/sql/articles.sql` `get-articles-for-feed` | Ordinary drift — not NEW-ADR (no incompatible architecture fork beyond implementing DESC newest-first) |

## Governance findings (F13–F14)

| ID | Check | Spec quote | Governing doc | Finding |
|----|-------|------------|---------------|---------|
| FF-01 | F13 | "Leave already-subscribed subscribe attempts as subscribed without requiring a distinct error" | NEW-ADR / REQ-23 / CTR-02 | `ALTERNATIVE: keep Conduit HTTP 400 on duplicate subscribe/unsubscribe state vs return idempotent success leaving graph unchanged per REQ-23 wire semantics` |
| FF-02 | F13 | "Omit seated-only subscription state for Guest profile reads" | NEW-ADR / REQ-22 / CTR-02 | `ALTERNATIVE: omit the following field on Guest profile responses vs emit following false as Conduit default for seated-only subscription state` |
| FF-03 | F14 | "Implementation architecture (chassis under `app/` vs `src/`), persistence, transport encoding) is **not** decided here — routed to feasibility / technical review." | ADR-001 / `architecture.mdc` | Spec correctly defers HOW; Accepted ADR-001 already locks Wave0a `app/` retention — INIT-002 continues unless a superseding ADR is opened |

## Findings by severity

### Critical

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| — | — | none | — |

### Should fix

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| FF-01 | F13 / F2 | NEW-ADR: duplicate subscribe/unsubscribe wire — Conduit 400 vs idempotent success (REQ-23) | Spec REQ-23; `profiles.py` raises `USER_IS_ALREADY_FOLLOWED` / `USER_IS_NOT_FOLLOWED`; unit expects 400 |
| FF-02 | F13 / F2 | NEW-ADR: Guest profile `following` omit vs emit `false` (REQ-22) | Spec REQ-22; `Profile.following` default False always in JSON; guest test asserts `not following` |
| FF-04 | F2 | Global listing not newest-first — drifts REQ-21 | `ArticlesRepository.filter_articles` limit/offset without ORDER BY |
| FF-05 | F2 | Subscription stream ordered `created_at` ascending — drifts REQ-21 newest-first | `articles.sql` `get-articles-for-feed` `ORDER BY a.created_at` |
| FF-06 | F2 / F4 | Unsubscribe→stream and publish-in/delete-out lifecycle lack dedicated unit coverage | No tests asserting feed membership after unfollow / create / delete; only empty + following-author membership |
| FF-07 | F11 / F9 | CTR-01..04 contract-test locations still “planned”; consumer (`realworld-web`) cannot lock against a named in-repo verify suite yet | Spec CTR table “planned under `tests/verify`” |

### Verify / Gap (informational)

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| FF-08 | F1 / F3 | No `tests/verify/` / `tests/README.md`; live CAP/J coverage planned only | Spec evidence layers; Makefile curl-only `verify` |
| FF-09 | F5 | As-built index absent — cannot assert live maturity for CAP-01..04 | Empty `docs/specification/as-built/`; spec A-08 |
| FF-10 | F6 / auto-fix | Spec index still says INIT-002 “awaiting Forge Draft PR” though Draft PR #11 is open | `docs/specification/README.md` Active product specs row |
| FF-03 | F14 | Chassis/MDC exception remains ADR-001-bound (informational continuity) | Accepted ADR-001; no `src/` tree |

## Impact surface

| Wave / area | Likely files/modules | Test touch |
|-------------|----------------------|------------|
| CAP-01 ungated discovery + REQ-21 global order | `app/api/routes/articles/articles_resource.py`, `app/db/repositories/articles.py` | unit list/order; live J-01..J-03, J-14 |
| CAP-02 subscribe stewardship + REQ-22/23 wire | `app/api/routes/profiles.py`, `app/models/domain/profiles.py`, `app/db/repositories/profiles.py` | unit follow/idempotent/guest profile; live J-04, J-09, J-13 |
| CAP-03 denials + empty stream | profiles follow guards; `articles_common.get_articles_for_user_feed` | unit self/missing/unauth; live J-07, J-08, J-10, J-12 |
| CAP-04 stream lifecycle + REQ-21 feed order | `articles.sql` `get-articles-for-feed`; articles create/delete | unit unfollow/publish/delete→feed; live J-05, J-06, J-11, J-15, J-16 |
| NEW-ADR wire (FF-01/FF-02) | Profile response schema + follow handlers | OpenAPI / consumer contract with web |
| Harness | `tests/verify/*`, `tests/README.md`, as-built index | live kill paths; CI vs live docs |
| Cross-repo CTR | API verify markers consumed by `realworld-web` | planned contract verify |

## Risks & assumptions

| ID | Risk / assumption | Mitigation |
|----|-------------------|------------|
| R-01 | Keeping Conduit 400 on duplicate follow breaks REQ-23 / consumer UAT | Resolve FF-01 in TDD; Accept NEW-ADR before plan |
| R-02 | Emitting `following: false` to Guests may be treated as “another member’s edges” disclosure or soft auth hint | Resolve FF-02 in TDD against REQ-22 / OQ-05 default |
| R-03 | Feed/global ordering ASC or unordered fails newest-first kill path with web | Plan TASKs for ORDER BY after TDD picks timestamp column(s) |
| R-04 | A-08 as-built absent — maturity of follow/feed beyond unit tests unknown | Publish as-built rows at ground / first wave |
| A-04 (spec) | Empty stream must not silently equal global | Baseline uses distinct `/articles/feed` vs `GET /articles` — keep endpoints separate |
| A-06 (spec) | Logout does not wipe subscription graph | ADR-004 + DB edges; prove reseat in live J-13 |
| IM-06 / Q-06 | Mid-view empty chrome without re-open | Deferred later; API next-open sufficient |
| IM-11 / Q-11 | Same-visit delete-out without re-open | Deferred later; REQ-18 next-open sufficient |

## Recommended spec edits

- Cite **Accepted ADR-001** (continue `app/`) under Assumptions / Q-12 resolution so chassis is not re-litigated as open PE unless superseding.
- After TDD, name the Chosen wire for REQ-22/REQ-23 in CTR-02 (omit vs false; idempotent vs 400) so web UAT language matches.
- Optionally cite planned verify module names once plan lands (do not invent coverage markers here).
- Do **not** expand INIT-002 into comments or follower **counts** despite residual Conduit surfaces.

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
| FF-01 | PE | Duplicate subscribe/unsubscribe: 400 vs idempotent success | yes | PE | open | technical review | Prefer idempotent success matching REQ-23 unless TDD Accepts Conduit-400 exception | REQ-23; `profiles.py` | pending NEW-ADR / TDD |
| FF-02 | PE | Guest `following` omit vs emit false | yes | PE | open | technical review | Omit seated-only field for Guest (REQ-22 / IM-05 default) | REQ-22; `Profile.following` | pending NEW-ADR / TDD |
| FF-04 | PE | Global listing newest-first ORDER BY | yes | PE | open | plan | ORDER BY updated_at/created_at DESC (INIT-001 REQ-34 family) | REQ-21; `filter_articles` | pending plan |
| FF-05 | PE | Subscription stream newest-first ORDER BY | yes | PE | open | plan | ORDER BY updated_at/created_at DESC (same family as FF-04) | REQ-21; `get-articles-for-feed` | pending plan |
| FF-06 | PE | Unit coverage for unfollow/publish-in/delete-out → stream | yes | PE | open | plan | Add focused unit cases before/with live J-06/J-11/J-16 | F2 partial rows | pending plan |
| FF-07 | PE | Name CTR verify suite location for api↔web | yes | PE | open | plan | `tests/verify` modules with `prayog:covers` for CTR-01..04 | Spec CTR table | pending plan |
| Q-06 | PM | Last-unsubscribe empty chrome without re-open | no | PM | open | later | Next open / re-check sufficient | IM-06 | Impact-Map IM-06 |
| Q-07 | PM | Clarification rounds per CTR vs PR thread | no | PM | open | later | Per product PR conversation; ≤2 rounds | IM-07 | programme process |
| Q-11 | PM | Delete-out same-visit without re-open | no | PM | open | later | Next open of stream after delete | IM-11; REQ-18 | Impact-Map IM-11 |
| Q-12 | PE | Chassis `app/` vs `src/` for INIT-002 | no | PE | resolved | technical review | Continue Accepted ADR-001 Option A | ADR-001; `app/` | `docs/specification/adr/adr-001-wave0a-package-chassis.md` |
| FF-08 | auto-fix | Add `tests/verify` + `tests/README.md` when plan names scripts | no | PE | open | plan | Document verify commands per CAP/J | F3 | pending plan |
| FF-09 | auto-fix | Seed as-built index rows as gap until waves close | no | PE | open | ground / first wave | Index rows = not implemented / unit-only | F5 / A-08 | pending |
| FF-10 | auto-fix | Update spec README status for open Draft PR #11 | no | PE | open | Forge publish | Status → Draft PR open (`spec-pending`) | `docs/specification/README.md` | pending Forge |
| FF-03 | auto-fix | Keep MDC/`src/` exception language tied to ADR-001 in future docs | no | PE | open | technical review | Cite ADR-001; do not imply `src/` migrate in INIT-002 | F14 | ADR-001 |

### PM questions (product scope, UX, priority)

#### Blocking — must resolve before spec merge
*(none — IM/OQ defaults already locked into REQs)*

#### Defer — can proceed with documented assumption
1. OQ-06 / IM-06 last-unsubscribe empty chrome without re-open — deferred later (non-blocking).
2. OQ-07 / IM-07 clarification-round counting — programme process only (non-blocking).
3. OQ-11 / IM-11 same-visit delete-out without re-open — deferred later (non-blocking).

### PE questions (engineering decisions — resolved by `/spec-technical-review`)

> These are **not** for PM. Run `/spec-technical-review` to produce a Technical
> Design Document that resolves these before `/spec-implementation-plan`.

#### Blocking for implementation plan
1. **FF-01** — `ALTERNATIVE: keep Conduit HTTP 400 on duplicate subscribe/unsubscribe state vs return idempotent success leaving graph unchanged per REQ-23 wire semantics`.
2. **FF-02** — `ALTERNATIVE: omit the following field on Guest profile responses vs emit following false as Conduit default for seated-only subscription state`.
3. **FF-04 / FF-05** — implement newest-first ordering for global listing and subscription stream (timestamp column choice in TDD notes).
4. **FF-06 / FF-07** — lifecycle unit coverage + named CTR verify suite placement.

#### Defer with default
1. Q-12 chassis — **resolved**: continue Accepted ADR-001 (`app/`).
2. Q-06 / Q-11 mid-view push — default: next open / re-check sufficient.

### Domain clarifications (business source-of-truth)

| # | Question | Suggested SME | Blocks |
|---|----------|---------------|--------|
| — | none | — | — |

### Auto-fixable (agent resolves later — not inside this skill)

| # | Item | Fix |
|---|------|-----|
| AF-1 | Missing `tests/README.md` / `tests/verify` scaffolding | Add when plan names verify scripts and covers markers |
| AF-2 | Empty as-built index | Seed capability rows as gap after first wave / at ground |
| AF-3 | Spec README still “awaiting Forge Draft PR” | Align status to open Draft PR #11 on next Forge publish |
| AF-4 | Q-12 open in product spec vs ADR-001 Accepted | Spec edit to mark Q-12 resolved citing ADR-001 (recommended; not applied in this read-only pass) |

---

## Check summary

| Check | Status | Findings |
|-------|--------|----------|
| F1 Baseline snapshot | PASS | Harness partial; as-built absent (FF-08/FF-09 informational) |
| F2 Spec → code map | FAIL | Follow/feed largely present; REQ-21/22/23 drifts FF-01/02/04/05; lifecycle unit gaps FF-06 |
| F3 Spec → verify map | PASS | Planned under `tests/verify` (FF-08 informational) |
| F4 Spec → unit map | PASS | Existing follow/feed tests; lifecycle gaps noted FF-06 |
| F5 As-built drift | PASS | No false “live” claims; A-08 notes absence (FF-09) |
| F6 Docs drift | PASS | AGENTS/rules present; README status stale (FF-10 informational) |
| F7 Overlap risk | PASS | Unit owns edge cases; live owns CAP/J journeys once verify exists |
| F8 CI vs live boundary | PASS | Pytest local/CI; Makefile curl verify; SDD verify not yet |
| F9 Cross-service touch | PASS | CTR-01..04 documented; contract tests planned (FF-07 Should-fix for naming) |
| F10 Assumptions | PASS | A-01..A-07/A-09 confirmed; A-08 open PE (as-built) |
| F11 Effort drivers | PASS | Wire ADRs; ordering; lifecycle prove; verify harness |
| F12 PM questions | PASS | Zero blocking PM |
| F13 ADR conformance | FAIL | NEW-ADR FF-01/FF-02; chassis/unseat aligned to Accepted ADR-001/004 |
| F14 MDC conformance | PASS | Chassis exception Accepted via ADR-001 (FF-03 informational) |

**Check PASS** = zero unresolved blocking findings (informational OK).

**Overall:** FAIL (blocking PE/ADR Should-fix) → workflow outcome `findings`.

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
| Local report path | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md` |
| Target branch | `docs/spec-init-realworld-002` (Draft PR [#11](https://github.com/drivestream-lab/realworld-api/pull/11), label `spec-pending`) |
| Recommended forge | `/commit-workspace` (Gate 2 stays `spec-pending`) |
| Mutations performed by this skill | **none** |

```
Draft spec PR: docs/spec-init-realworld-002  (spec-pending) — https://github.com/drivestream-lab/realworld-api/pull/11
When ready:
  [ ] Source freshness is CURRENT
  [ ] All blocking PM questions answered on meta PRD PR
  [ ] All blocking Domain clarifications answered and published via Forge
  [ ] Spec updated to reflect answers (same branch, via Forge)
  [ ] Incremental re-run of /initiative-feasibility on updated spec is clean
  [ ] Proceed: /spec-technical-review (always — pin routes pass and findings here)
  [ ] After spec + feasibility + TDD (if any) + plan on branch (Forge publish):
      PE sets spec-lgtm + Approve on exact head → Ready for review → merge
  [ ] After merge: `/create-board-tickets` from plan §9 — then /pre-implement → /loop-spec
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: initiative-feasibility
  outcome: findings
  artifact:
    path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md
  blockers:
    - FF-01
    - FF-02
    - FF-04
    - FF-05
    - FF-06
    - FF-07
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92
    scope_digest: sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0
    meta_pr_approved_head: ee9fe45ad23d988eface7517a3a65a7b58b592c1
    ripple_action: continue
    new_adr: true
    new_adr_ids:
      - FF-01
      - FF-02
    draft_adr_paths: []
    lane_counts:
      pm_blocking_open: 0
      pe_blocking_open: 6
      domain_blocking_open: 0
      auto_fix_open: 4
    severity_counts:
      critical: 0
      should_fix: 6
      verify_gap: 4
    draft_spec_pr: https://github.com/drivestream-lab/realworld-api/pull/11
    codegraph_provider: degraded-none
    grounding_depth: none
    outcome_rationale: unresolved blocking PE/ADR Should-fix items including NEW-ADR subscribe idempotency and Guest following wire; REQ-21 ordering drifts
  next_candidates:
    - spec-technical-review
  human_checkpoint: false
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-002] Spec — realworld-api (feasibility)"
    body_path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md
    target_branch: docs/spec-init-realworld-002
```
