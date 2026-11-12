# Feasibility report — INIT-REALWORLD-001

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-001 |
| Spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| PRD digest | `sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4` |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-001.md` / `1` |
| Repo scope digest | `sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d` |
| Approved meta PR head | `a500df8eeefbea095ecdd65e00edb128416c3cf4` |
| Impact-map approval | Review `PRR_kwDOVac9Rs8AAAABW9LPzQ` / id `5835509709` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T01:45:11Z`; `commit_id` = `a500df8eeefbea095ecdd65e00edb128416c3cf4` (meta PR [#5](https://github.com/drivestream-lab/realworld-meta/pull/5) MERGED; label `impact-map-lgtm`) |
| Source freshness | CURRENT — H1 live PRD digest matches spec citation; H2 api scope digest recomputed match; H3 `map_revision=1`; G1 APPROVED review `commit_id` equals merged meta PR #5 head; ripple `continue` |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-11 |
| Branch | `docs/spec-init-realworld-001` — Draft spec PR [#3](https://github.com/drivestream-lab/realworld-api/pull/3) (`spec-pending`) |
| Initiative segment | `INIT-REALWORLD-001` |
| Status | Draft |
| Review deadline | 2026-11-16 |
| Deciders | PM: programme PM · Domain SME: @drivestream-lab/backend-devs |
| Re-run note | Incremental re-evaluation after local Draft ADR-001..004 appeared; Accepted ADR SSOT still empty — PE blockers reconfirmed against `app/` |

## Summary

The Wave0a API provider spec is **buildable** against the legacy Conduit FastAPI baseline under `app/`, but **not clean for plan** until PE resolves architecture alternatives and baseline drifts. Source freshness is **CURRENT**. Draft ADR-001..004 exist locally and propose chassis / shelf / favoritesCount / unseat choices, but they are **not Accepted** — F13 still treats Accepted ADR coverage as missing. Blocking PE/ADR items remain (Critical + Should-fix). Proceed to `/spec-technical-review` (outcome `findings`); do not set `spec-lgtm`.

**Findings:** 14 total (2 Critical, 9 Should fix, 3 Verify / Gap)

### Derived counts (lane × severity)

| Lane | Blocking open | Non-blocking open | Resolved |
|------|---------------|-------------------|----------|
| PM | 0 | 0 | 8 (Q-01..Q-04, Q-06..Q-08 + IM defaults) |
| PE / ADR | 11 | 2 (Q-05, Q-09 deferred later) | 0 |
| Domain | 0 | 0 | 0 |
| Auto-fix | 0 | 3 | 0 |

| Severity | Unresolved count |
|----------|------------------|
| Critical | 2 |
| Should fix | 9 |
| Verify / Gap (informational) | 3 |

### Selected workflow outcome

| Field | Value |
|-------|-------|
| Outcome | `findings` |
| Rationale | Unresolved blocking PE/ADR items (Critical + Should-fix PE-lane); Draft ADRs not Accepted; baseline privacy/tag/seat drifts remain |
| Next (from workflow) | `spec-technical-review` |

Informational observations alone do **not** select `findings`. Unresolved
blocking PE/ADR → `findings`; blocking PM/domain → `needs-input`.

## Baseline snapshot (F1)

| Area | Current state | Evidence |
|------|---------------|----------|
| Unit / in-process tests | Present under `tests/test_api/`, `tests/test_services/`, `tests/test_schemas/`, `tests/test_db/` (not `tests/unit/`). Pytest + asyncio in `pyproject.toml`. Covers registration, login, articles CRUD/favorite filters, profiles, comments, JWT. | `tests/test_api/test_routes/test_articles.py`, `test_registration.py`, `test_login.py`, `pyproject.toml` `[tool.pytest.ini_options]` |
| Live verify | **Absent** as SDD `tests/verify/` + `tests/README.md`. Makefile `verify` is a single host curl to `localhost:3100/api/articles` (overlay/local prove). | `Makefile` `verify` target; no `tests/verify/`; no `tests/README.md` |
| As-built | **Absent** — `docs/specification/as-built/` empty; index path missing | Spec A-09; empty `docs/specification/as-built/` |
| Source layout | Legacy Conduit package under `app/` (FastAPI routes, asyncpg repos, Alembic). **No** `src/` tree despite profile `source_roots: [src/]` and platform MDC. | `app/main.py`, `app/api/routes/api.py`; `.harness/profile.yaml` |
| Toolchain | Poetry; black; pytest; Makefile `verify` only (no `make check` / pyright / import-linter yet) | `pyproject.toml`, `Makefile` |
| ADRs | Draft ADR-001..004 present; **zero Accepted** | `docs/specification/adr/adr-001-*.md` … `adr-004-*.md` (Status: Draft) |

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | Package chassis / `app/` vs `src/` | Draft — not Accepted (FF-01) |
| ADR-002 | Private-shelf `favorited=` authorization | Draft — not Accepted (FF-02) |
| ADR-003 | Public `favoritesCount` wire policy | Draft — not Accepted (FF-03) |
| ADR-004 | Unseat via client JWT discard | Draft — not Accepted (FF-04) |

Accepted ADR constraint set for F13: **empty** (Draft files are not SSOT).

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout, JWT verify, `src/` packages, service naming | read |
| `dependency-injection.mdc` | injector lifecycle | read |
| `infra-services.mdc` | DB / outbound clients | read |
| `repository-pattern.mdc` | repo ↔ ORM boundary | read |
| `pydantic-schemas.mdc` | models in `src/models/` | read |
| `http-api-conventions.mdc` | body vs query | read |
| `fail-fast.mdc` | no silent fallbacks | read |
| `testing-verify-flows.mdc` | verify / pytest split | read |
| `python-tooling.mdc` | make check / pyright | read |
| `database-migrations.mdc` | Alembic scripts | read |
| `strong-typing.mdc` | typing boundaries | read |
| `python-imports.mdc` | import policy | skim |
| `logging-loguru.mdc` | structured logging | skipped — NFR observability N/A as kill criterion |
| `spec-driven-development.mdc` | SDD discipline | skim |
| `code-guidelines-index.mdc` | index | skim |

## Traceability matrix

| Spec REQ / wave | Spec claim | Code evidence | Unit | Verify | Status |
|-----------------|------------|---------------|------|--------|--------|
| REQ-01 / CAP-01 | Guest global feed ungated | `app/api/routes/articles/articles_resource.py` `list_articles` + `get_current_user_authorizer(required=False)` | partial (`test_articles.py` list) | planned | partial |
| REQ-02 / CAP-01 | Guest open article | `retrieve_article_by_slug` (no required auth) | partial | planned | partial |
| REQ-03 / CAP-01 | Tag lane | `list_articles` `tag=` filter | partial | planned | partial |
| REQ-04 / CAP-01 | Public profile | `app/api/routes/profiles.py` `retrieve_profile_by_username`; author filter on articles | partial (`test_profiles.py`) | planned | partial |
| REQ-05–06 / CAP-01 | Multi-tag hop | create links multiple tags (`create_article` + `articles_to_tags`) | partial (tag create test) | planned | partial |
| REQ-07 / CAP-01 | Read after unseat | Reads never require seat; logout is client token drop today | gap (no logout API) | planned | partial |
| REQ-08–09 / CAP-02 | Register + uniqueness | `authentication.py` `register`; username/email taken checks | exists (`test_registration.py`) | planned | partial — **register also issues JWT** (drift vs IM-04) |
| REQ-10–11 / CAP-02 | Login seat / refuse | `authentication.py` `login` | exists (`test_login.py`) | planned | exists |
| REQ-12–13 / CAP-02 | Logout unseat / reseat | **No logout route**; JWT client discard assumed | gap | planned | gap |
| REQ-14 / CAP-02 | Unseated deny | Mutations use `get_current_user_authorizer()` | partial | planned | partial |
| REQ-15–18 / CAP-03 | Tagged publish / refuse | `create_new_article`; tags optional default `[]` | partial (create without tags succeeds in tests) | planned | **drift** vs ≥1 tag |
| REQ-19 / CAP-03 | No server draft | No draft tables/routes observed | gap | planned | exists (absence) |
| REQ-20–22 / CAP-04 | Edit + tag-set / zero-tag refuse | `update_article_by_slug`; `ArticleInUpdate` **has no tagList**; repo `update_article` no tags | gap | planned | **gap** |
| REQ-23–24 / CAP-04 | Delete own / peer deny | `delete_article_by_slug` + `check_article_modification_permissions` | partial | planned | exists |
| REQ-25–26 / CAP-05 | Favorite / unfavorite | `articles_common.py` mark/unmark favorite | partial | planned | partial |
| REQ-27 / CAP-05 | Shelf isolation | Public `?favorited=username` on `list_articles` **exposes any member’s favorites** (`test_filtering_by_favorited`) | exists (wrong polarity) | planned | **drift / conflict** |
| REQ-28 / CAP-05 | Refuse own favorite | `mark_article_as_favorite` — **no author check** | gap | planned | gap |
| REQ-29 / CAP-05 | Unseated favorite deny | Auth required on favorite routes | partial | planned | partial |
| REQ-30–32 / CAP-06 | Nameplate self-update / peer deny / unseat | `users.py` `update_current_user` (auth required; **allows username/email change**) | partial | planned | **drift** vs identity-lock |
| REQ-33 / CAP-05 | No resurrection after delete | Delete removes article; favorite of missing → 404 via path dep | partial | planned | partial |
| REQ-34 / CAP-01 | Newest-first feed | `filter_articles` builds query with limit/offset **without ORDER BY** | gap | planned | gap |
| REQ-35 / CAP-05 | Favorite missing/deleted fail-closed | Path lookup 404 before favorite | partial | planned | partial |
| OOS comments / feed / follow | Non-goals present in baseline | `comments.py`, `articles_common.get_articles_for_user_feed`, `profiles` follow routes | exists (OOS) | N/A | residual surface |

## ADR traceability (F13)

| Spec REQ / wave | Relevant ADR(s) | Status | Code evidence | Finding |
|-----------------|-----------------|--------|----------------|---------|
| CAP-01..06 / Q-10 | NEW-ADR (Draft ADR-001 pending) | missing ADR | `app/main.py`, `app/api/routes/api.py` (legacy chassis; no `src/`) | `ALTERNATIVE: retain and harden legacy Conduit package under app/ for Wave0a vs migrate provider onto platform src/ chassis (DI + layered layout per architecture.mdc)` |
| REQ-27 / CTR-05 | NEW-ADR (Draft ADR-002 pending) | missing ADR | `app/api/routes/articles/articles_resource.py` `favorited` filter; `tests/test_api/test_routes/test_articles.py` `test_filtering_by_favorited` | `ALTERNATIVE: keep public Conduit favorited=username list filter vs restrict private-shelf listing to the seated owner only (fail-closed for peers/guests)` |
| REQ-25 / non-goal social proof | NEW-ADR (Draft ADR-003 pending) | missing ADR | `app/models/domain/articles.py` `favorites_count`; favorite routes increment count | `ALTERNATIVE: omit or zero-out public favoritesCount (and peer shelf discovery) for Wave0a privacy vs retain full Conduit RealWorld wire fields for client compatibility` |
| REQ-12 / CTR-02 | NEW-ADR (Draft ADR-004 pending) | missing ADR | no logout route under `app/api/routes/`; JWT via `app/services/jwt.py` | `ALTERNATIVE: treat client JWT discard as Wave0a unseat (no server revoke) vs add server-side session/token revocation on logout` |

## Governance findings (F13–F14)

| ID | Check | Spec quote | Governing doc | Finding |
|----|-------|------------|---------------|---------|
| FF-01 | F13 | "Implementation architecture (chassis under `app/` vs `src/`), persistence, transport encoding) is **not** decided here — routed to feasibility / technical review." | NEW-ADR / Draft ADR-001 / `architecture.mdc` | `ALTERNATIVE: retain and harden legacy Conduit package under app/ for Wave0a vs migrate provider onto platform src/ chassis (DI + layered layout per architecture.mdc)` |
| FF-02 | F13 | "Keep one member’s private shelf invisible to another member" | NEW-ADR / Draft ADR-002 / REQ-27 | `ALTERNATIVE: keep public Conduit favorited=username list filter vs restrict private-shelf listing to the seated owner only (fail-closed for peers/guests)` |
| FF-03 | F13 | "no public who-favorited social proof is shown" | NEW-ADR / Draft ADR-003 / REQ-25 | `ALTERNATIVE: omit or zero-out public favoritesCount (and peer shelf discovery) for Wave0a privacy vs retain full Conduit RealWorld wire fields for client compatibility` |
| FF-04 | F13 | "Unseat on logout and revoke contribution actions" | NEW-ADR / Draft ADR-004 / REQ-12 | `ALTERNATIVE: treat client JWT discard as Wave0a unseat (no server revoke) vs add server-side session/token revocation on logout` |
| FF-05 | F14 | "this spec states observable API product behavior… Implementation architecture… is **not** decided here" | `architecture.mdc` (`src/` packages, AuthMiddleware, DI) | Spec correctly defers chassis; baseline `app/` conflicts with MDC if retained without Accepted ADR — same decision as FF-01 |

## Findings by severity

### Critical

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| FF-01 | F13 | NEW-ADR required: chassis choice blocks plan-quality TASK placement and MDC conformance path (Draft ADR-001 not Accepted) | Spec Q-10; Draft `docs/specification/adr/adr-001-wave0a-package-chassis.md`; `app/` vs profile `source_roots: [src/]` + `architecture.mdc` |
| FF-02 | F2 / F13 | Baseline public `?favorited=` listing contradicts REQ-27 shelf isolation — must be decided/fixed before Wave0a privacy prove (Draft ADR-002 not Accepted) | Spec REQ-27; `list_articles` favorited filter; `test_filtering_by_favorited` |

### Should fix

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| FF-03 | F13 | NEW-ADR: public `favoritesCount` vs Wave0a no social-proof non-goal (Draft ADR-003 not Accepted) | `Article.favorites_count`; favorite handlers mutate count |
| FF-04 | F13 | NEW-ADR: logout/unseat mechanism for API provider (Draft ADR-004 not Accepted) | No logout route; REQ-12 / CTR-02 |
| FF-05 | F2 / F10 | Register issues JWT immediately — drifts from IM-04 / REQ-08 “eligibility only; seat via login” | `authentication.py` `register` returns `UserWithToken` |
| FF-06 | F2 | Article update schema/repo cannot change tags — blocks REQ-20/21/22 as written | `ArticleInUpdate` lacks tags; `ArticlesRepository.update_article` no tag params |
| FF-07 | F2 | Zero-tag publish allowed — drifts from REQ-16 | `ArticleInCreate.tags` default `[]`; create tests omit tags |
| FF-08 | F2 | Own-article favorite not refused — drifts from REQ-28 | `mark_article_as_favorite` no author check |
| FF-09 | F2 | Profile self-update allows username/email mutation — drifts from REQ-30 identity-lock | `UserInUpdate` + `update_current_user` |
| FF-10 | F2 | Global feed ordering not newest-first — drifts from REQ-34 | `filter_articles` has no ORDER BY |
| FF-11 | F14 | MDC `src/` chassis patterns unmet by baseline `app/` (resolved only via Accepted ADR for FF-01) | `architecture.mdc`, `dependency-injection.mdc`, `pydantic-schemas.mdc` |

### Verify / Gap (informational)

| ID | Check | Finding | Evidence |
|----|-------|---------|----------|
| FF-12 | F1 / F3 | No `tests/verify/` / `tests/README.md`; live coverage planned only | Spec CTR contract-test “planned”; Makefile curl-only `verify` |
| FF-13 | F5 | As-built index absent — cannot assert live maturity rows | Empty `docs/specification/as-built/`; spec A-09 |
| FF-14 | F7 / F9 | OOS Conduit surfaces (comments, personalized feed, follow) coexist with Wave0a scope — verify must not treat them as CAP prove; CTR contract suites still planned | `comments.py`, `/articles/feed`, profiles follow routes |

## Impact surface

| Wave / area | Likely files/modules | Test touch |
|-------------|----------------------|------------|
| CAP-01 bulletin read + REQ-34 order | `app/api/routes/articles/*`, `app/db/repositories/articles.py` | unit list/order; live J-01/J-02/J-04 |
| CAP-02 seat lifecycle | `app/api/routes/authentication.py`, `users.py`, `app/api/dependencies/authentication.py`, `app/services/jwt.py` | unit login/register; live J-05..J-08, J-11 |
| CAP-03 publish + tag rules | `articles_resource.py`, `app/models/schemas/articles.py`, tags repo | unit zero-tag; live J-06/J-12/J-18 |
| CAP-04 revise/delete + tag edit | schemas + articles repo update path (needs tag update capability) | unit ownership/zero-tag; live J-09/J-10/J-15 |
| CAP-05 private shelf privacy | favorite routes + `favorited` filter policy + response shape | unit own-favorite/peer isolation; live J-13/J-16 |
| CAP-06 nameplate | `app/api/routes/users.py`, `UserInUpdate` | unit identity-lock; live J-13/J-19 |
| Chassis / ADR (if migrate) | new `src/**` per platform rules; DI modules; migrations bridge | tooling `make check`; broad regression |
| Harness | `tests/verify/*`, `tests/README.md`, as-built index | live kill paths; CI boundary docs |
| Cross-repo CTR | API OpenAPI / verify markers consumed by `realworld-web` | planned contract verify |

## Risks & assumptions

| ID | Risk / assumption | Mitigation |
|----|-------------------|------------|
| R-01 | Retaining `app/` without Accepted ADR leaves permanent MDC conflict | Resolve FF-01 in TDD; Accept ADR-001 before plan |
| R-02 | Conduit wire compatibility (`favorited`, `favoritesCount`, register token) vs Wave0a privacy/seat locks | Resolve FF-02/FF-03/FF-05 with web consumer; Accept ADR-002/003 |
| R-03 | Tag-set edit absent in baseline — CAP-04 incomplete without schema/repo work | Explicit TASK in plan after TDD |
| R-04 | A-09 as-built absent — maturity unknown beyond source scan | Publish as-built index stub at ground / first wave |
| A-04 (spec) | Explicit logout defines unseat; idle timeout not required | Default FF-04 to client JWT discard (Draft ADR-004 Option A) unless PE Accepts otherwise |
| IM-05 / Q-05 | Multi-session cascade out of scope | Defer; Wave0a proves logging-out client only |
| IM-09 / Q-09 | Mid-read push not required | Defer; not-found on reopen |

## Recommended spec edits

- Add a short **API unseat semantics** note under CAP-02 / CTR-02: whether Wave0a API treats client token discard as sufficient logout (align with FF-04 / Draft ADR-004) so web/local prove language stays unambiguous.
- Clarify **register response**: if IM-04 eligibility-only is strict, note that issuance of a session token at register is non-conformant and must not be relied on for kill-path “authenticate”; else record an accepted exception.
- Optionally cite planned verify module names once TDD/plan lands (do not invent coverage markers here).
- Do **not** expand Wave0a into comments / follow / personalized feed despite baseline routes.

---

## Open items by lane

| ID | Lane | Question / item | Blocking | Owner | Status | Required by | Default if deferred | Evidence | Resolution reference |
|----|------|-----------------|----------|-------|--------|-------------|---------------------|----------|----------------------|
| FF-01 | PE | Chassis: `app/` vs platform `src/` | yes | PE | open | technical review | Satisfy REQs regardless of chassis; Accepted ADR required before plan TASK placement | Spec Q-10; `app/main.py` | Draft `docs/specification/adr/adr-001-wave0a-package-chassis.md` (pending Accept) |
| FF-02 | PE | Private shelf listing vs public `favorited=` filter | yes | PE | open | technical review | Restrict shelf listing to seated owner; fail-closed for peers/guests | REQ-27; `test_filtering_by_favorited` | Draft `docs/specification/adr/adr-002-private-shelf-list-authorization.md` (pending Accept) |
| FF-03 | PE | Public `favoritesCount` vs no social proof | yes | PE | open | technical review | Zero-out count for Wave0a UAT; no who-favorited lists | REQ-25; `favorites_count` | Draft `docs/specification/adr/adr-003-favorites-count-wire-policy.md` (pending Accept) |
| FF-04 | PE | Logout/unseat API mechanism | yes | PE | open | technical review | Client JWT discard = unseat; no server revoke in Wave0a | REQ-12; no logout route | Draft `docs/specification/adr/adr-004-wave0a-unseat-token-discard.md` (pending Accept) |
| FF-05 | PE | Register returns token vs eligibility-only | yes | PE | open | technical review | Kill-path prove uses login; treat register token as non-authoritative until TDD decides strip vs keep | IM-04; `register` | pending TDD |
| FF-06 | PE | Tag-set update missing on article update | yes | PE | open | technical review | Extend update contract to accept tagList with ≥1 non-blank rule | `ArticleInUpdate` | pending TDD |
| FF-07 | PE | Enforce ≥1 non-blank tag on create | yes | PE | open | plan | Reject empty/blank-only tagList | REQ-16; create schema default `[]` | pending plan |
| FF-08 | PE | Refuse favorite of own article | yes | PE | open | plan | Fail closed; shelf unchanged | REQ-28 | pending plan |
| FF-09 | PE | Identity-lock username/email on self-update | yes | PE | open | plan | Bio/image only editable | REQ-30; `UserInUpdate` | pending plan |
| FF-10 | PE | Newest-first global feed ordering | yes | PE | open | plan | ORDER BY updated_at/created_at DESC | REQ-34; `filter_articles` | pending plan |
| FF-11 | PE | MDC conformance path tied to chassis ADR | yes | PE | open | technical review | Same as FF-01 | `architecture.mdc` | Draft ADR-001 (pending Accept) |
| Q-05 | PE | Multi-session logout cascade | no | PE | open | later | Unseat logging-out session only | IM-05 | Impact-Map IM-05 |
| Q-09 | PE | Mid-read refresh after delete | no | PE | open | later | Next navigation / reopen sufficient | IM-09 | Impact-Map IM-09 |
| FF-12 | auto-fix | Add `tests/verify` + `tests/README.md` feature map when plan names scripts | no | PE | open | plan | Document verify commands per CAP/J | F3 | pending plan |
| FF-13 | auto-fix | Seed as-built index rows as gap until waves close | no | PE | open | ground / first wave | Index rows = not implemented | F5 / A-09 | pending |
| FF-14 | auto-fix | Exclude OOS routes from Wave0a verify covers | no | PE | open | plan | Do not list comments/follow/feed in covers | F7/F9 | pending plan |

### PM questions (product scope, UX, priority)

#### Blocking — must resolve before spec merge
*(none — IM/OQ defaults already locked into REQs)*

#### Defer — can proceed with documented assumption
1. OQ-05 / IM-05 multi-session cascade — deferred later (non-blocking).
2. OQ-09 / IM-09 mid-read push — deferred later (non-blocking).

### PE questions (engineering decisions — resolved by `/spec-technical-review`)

#### Blocking for implementation plan
1. **FF-01** — `ALTERNATIVE: retain and harden legacy Conduit package under app/ for Wave0a vs migrate provider onto platform src/ chassis (DI + layered layout per architecture.mdc)`.
2. **FF-02** — `ALTERNATIVE: keep public Conduit favorited=username list filter vs restrict private-shelf listing to the seated owner only (fail-closed for peers/guests)`.
3. **FF-03** — `ALTERNATIVE: omit or zero-out public favoritesCount (and peer shelf discovery) for Wave0a privacy vs retain full Conduit RealWorld wire fields for client compatibility`.
4. **FF-04** — `ALTERNATIVE: treat client JWT discard as Wave0a unseat (no server revoke) vs add server-side session/token revocation on logout`.
5. **FF-05..FF-10** — baseline drift items (register token, tag update, zero-tag, own-favorite, identity-lock, feed order) to disposition in TDD then plan TASKs.

#### Defer with default
1. Q-05 multi-session cascade — default: logging-out session only.
2. Q-09 mid-read refresh — default: reopen/not-found sufficient.

### Domain clarifications (business source-of-truth)

| # | Question | Suggested SME | Blocks |
|---|----------|---------------|--------|
| — | none | — | — |

### Auto-fixable (agent resolves later — not inside this skill)

| # | Item | Fix |
|---|------|-----|
| AF-1 | Missing `tests/README.md` / `tests/verify` scaffolding | Add when plan names verify scripts and covers markers |
| AF-2 | Empty as-built index | Seed capability rows as gap after first wave / at ground |
| AF-3 | Spec PR body helper already on branch | Keep `docs/specification/reports/Spec-PR-Body-INIT-REALWORLD-001-realworld-api.md` aligned on Forge publish |

---

## Check summary

| Check | Status | Findings |
|-------|--------|----------|
| F1 Baseline snapshot | PASS | Harness partial; as-built absent (FF-13 informational) |
| F2 Spec → code map | FAIL | Partial map; privacy/tag/seat drifts FF-02, FF-05..FF-10 |
| F3 Spec → verify map | PASS | Planned under `tests/verify` (FF-12 informational) |
| F4 Spec → unit map | PASS | Existing `tests/test_*`; Wave0a denial gaps remain |
| F5 As-built drift | PASS | No false “live” claims; A-09 notes absence (FF-13) |
| F6 Docs drift | PASS | AGENTS/rules present; Accepted ADR empty → NEW-ADR via F13 (Draft ADR files noted) |
| F7 Overlap risk | PASS | Note OOS route residual (FF-14); avoid dual journey ownership later |
| F8 CI vs live boundary | PASS | Pytest local/CI; Makefile curl verify; SDD verify not yet |
| F9 Cross-service touch | PASS | CTR-01..06 documented; contract tests planned |
| F10 Assumptions | PASS | A-01..A-08 confirmed; A-09 open PE |
| F11 Effort drivers | PASS | Chassis; privacy wire; tag update; seat semantics; verify harness |
| F12 PM questions | PASS | Zero blocking PM |
| F13 ADR conformance | FAIL | NEW-ADR FF-01..FF-04; Draft ADR-001..004 not Accepted |
| F14 MDC conformance | FAIL | Chassis/MDC mismatch until FF-01 Accepted (FF-11) |

**Check PASS** = zero unresolved blocking findings (informational OK).

**Overall:** FAIL (blocking PE/ADR) → workflow outcome `findings`.

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
| Local report path | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md` |
| Target branch | `docs/spec-init-realworld-001` (Draft PR [#3](https://github.com/drivestream-lab/realworld-api/pull/3), label `spec-pending`) |
| Recommended forge | `/commit-workspace` (Gate 2 stays `spec-pending`) |
| Mutations performed by this skill | **none** |

```
Draft spec PR: docs/spec-init-realworld-001  (spec-pending) — https://github.com/drivestream-lab/realworld-api/pull/3
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
    path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md
  blockers:
    - FF-01
    - FF-02
    - FF-03
    - FF-04
    - FF-05
    - FF-06
    - FF-07
    - FF-08
    - FF-09
    - FF-10
    - FF-11
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4
    scope_digest: sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d
    meta_pr_approved_head: a500df8eeefbea095ecdd65e00edb128416c3cf4
    ripple_action: continue
    new_adr: true
    new_adr_ids:
      - FF-01
      - FF-02
      - FF-03
      - FF-04
    draft_adr_paths:
      - docs/specification/adr/adr-001-wave0a-package-chassis.md
      - docs/specification/adr/adr-002-private-shelf-list-authorization.md
      - docs/specification/adr/adr-003-favorites-count-wire-policy.md
      - docs/specification/adr/adr-004-wave0a-unseat-token-discard.md
    lane_counts:
      pm_blocking_open: 0
      pe_blocking_open: 11
      domain_blocking_open: 0
      auto_fix_open: 3
    severity_counts:
      critical: 2
      should_fix: 9
      verify_gap: 3
    draft_spec_pr: https://github.com/drivestream-lab/realworld-api/pull/3
    codegraph_provider: degraded-none
    grounding_depth: none
    outcome_rationale: unresolved blocking PE/ADR findings including NEW-ADR chassis and private-shelf wire privacy; Draft ADRs not Accepted
  next_candidates:
    - spec-technical-review
  human_checkpoint: false
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-001] Spec — realworld-api (feasibility)"
    body_path: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md
    target_branch: docs/spec-init-realworld-001
```
