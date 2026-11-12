---
goal: INIT-REALWORLD-002 — implementation plan
initiative: INIT-REALWORLD-002
status: Planned
date_created: 2026-11-12
source_spec: docs/specification/product/INIT-REALWORLD-002-api.md
feasibility_report: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md
technical_review: docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md
prd_digest: sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92
impact_map: realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-002.md
impact_map_revision: 1
repo_scope_digest: sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0
approved_meta_pr_head: ee9fe45ad23d988eface7517a3a65a7b58b592c1
branch: docs/spec-init-realworld-002
review_deadline: 2026-11-17
deciders: PE — spec-lgtm + Approve on exact head after full package
---

# Implementation plan — INIT-REALWORLD-002

## Source freshness and command contract

| Item | Value | Status |
|------|-------|--------|
| Spec | `docs/specification/product/INIT-REALWORLD-002-api.md` | CURRENT — digest `sha256:b6d9a028486a5f94c6e4f5d42bd539584ed35091d5b71f7f8665f5fb47b79b4a` matches live file; H1 PRD digest matches meta PRD |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md` | CURRENT — cites same H1/H2/H3/G1; tip continuous into Accepted TDD |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md` | CURRENT — `Status: Accepted`; ADR-005/006 Accepted with plan-time Lint evidence; ready_for_plan=YES |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-002.md` / `1` | CURRENT |
| Repo scope digest | `sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0` | CURRENT — api row CAP-01..CAP-04 |
| Approved meta PR head | `ee9fe45ad23d988eface7517a3a65a7b58b592c1` | CURRENT — meta PR #8 |
| `check_command` | `make check` | RESOLVED — W0 co-ships Makefile `check` target (`poetry run black --check app tests`); ADR-001 allows incremental tooling vs full pyright/import-linter |
| `test_command` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | RESOLVED |
| `verify_command` | Wave-scoped live modules under `tests/verify/` (W0 `poetry run python -m tests.verify.verify_wave0_subscription_stewardship`; W1 `poetry run python -m tests.verify.verify_wave1_discovery_stream`) | RESOLVED — co-shipped with product surface (P15); not unit |
| `ground_command` | N/A — as-built seeded in W1; `/ground-spec` after wave-acceptance (AF-2) | N/A — reason recorded |

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md` |
| Technical review status | Accepted |
| PE sign-off | [x] complete — 2026-11-12 (Buzz `accept tdd-adr`; ADR-005/006 Lint evidence finalized on Draft PR head `93cedca068c2940e034d06d6b1ba24bcfbc3beda`) |
| Resolved ADRs | [`docs/specification/adr/adr-005-idempotent-subscribe-wire.md`](../adr/adr-005-idempotent-subscribe-wire.md) (Accepted); [`docs/specification/adr/adr-006-guest-following-field-omit.md`](../adr/adr-006-guest-following-field-omit.md) (Accepted). Constraining baseline: [`adr-001-wave0a-package-chassis.md`](../adr/adr-001-wave0a-package-chassis.md) (Accepted — continue `app/`); [`adr-004-wave0a-unseat-token-discard.md`](../adr/adr-004-wave0a-unseat-token-discard.md) (Accepted — reseat persistence). ADR-002/003 independent (shelf / favoritesCount). |
| ADR product-boundary re-check | ADR-005 and ADR-006: `changes_user_visible_behavior: false` / `spec_amendment_required: false`. Plan-time `adr_boundary_lint.py --strict --verify-lint-evidence` **PASS** (ADR-005 `sha256:7fc921cfa52e6cf035acfa44fbfa27da9bb0a527e953a9d9c157916196f67dfa`; ADR-006 `sha256:bf81fe7fc238bc8c595ebff37167b76b65e6b830b1d7aebd770cee9b703b17d4`) with sources reconstructed from spec REQ rows + feasibility Spec quotes + FF finding texts |
| Outstanding PM questions | none blocking — Q-06 / Q-07 / Q-11 deferred later with defaults (next-open / programme process) |
| Outstanding domain questions | none — all resolved |

> Do not start W0 implementation until PE sign-off is marked complete above.

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | package chassis / `app/` vs `src/` | Accepted — continue |
| ADR-002 | private-shelf `favorited=` authorization | Accepted — out of INIT-002 CAP scope |
| ADR-003 | `favoritesCount` wire policy | Accepted — counts non-goal here |
| ADR-004 | unseat via client JWT discard | Accepted — REQ-09 persistence |
| ADR-005 | idempotent same-state subscribe POST | Accepted — REQ-23 / REQ-07 |
| ADR-006 | Guest profile omits `following` | Accepted — REQ-22 / REQ-04 |

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout / JWT / packages | read — Wave0a exception via Accepted ADR-001 |
| `fail-fast.mdc` | denial / no silent fallback | read — empty-stream / fail-closed denials |
| `http-api-conventions.mdc` | body/query/path | read |
| `repository-pattern.mdc` | repo boundary | read — `app/db/repositories` under ADR-001 |
| `pydantic-schemas.mdc` | schemas | read — `app/models` under ADR-001 |
| `testing-verify-flows.mdc` | verify vs pytest | read — FF-08 / P15 |
| `python-tooling.mdc` | make check | read — incremental `make check` in W0 |
| `dependency-injection.mdc` | injector | skipped — ADR-001 retains `app/` without injector migrate |
| `infra-services.mdc` | pools/clients | skipped — no new infra client |
| `logging-loguru.mdc` | logging | skipped — NFR observability N/A as kill criterion |
| others | — | skipped — not in INIT-002 TASK touch set |

### P15 overlap check (recorded)

| Query | Result | Disposition |
|-------|--------|-------------|
| `PYTHONPATH=prayog-skills:. python3 prayog-skills/scripts/verify_coverage_query.py tests/verify --dump` | `error: not a directory: tests/verify` | **New** live verify FILEs warranted (FF-08 / AF-1) |
| `--capability CAP-01` .. `CAP-04` | same — dir absent | **New** fixture packs under `tests/fixtures/` warranted |
| `--journey J-04` / `J-05` / `J-08` / `J-14` | same — dir absent | **New** journey fixture packs warranted |

---

## 1. Requirements (REQ) — product ids

| ID | Summary | Spec path | Waves |
|----|---------|-----------|-------|
| REQ-01 | Guest public article listing ungated | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-02 | Guest open published article ungated | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-03 | Guest public tags / empty unknown lane | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-04 | Subscribe affordance must not gate public reads | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0, W1 |
| REQ-05 | Public discovery membership independent of subscriptions | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-06 | Seated global listing subscription-independent | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-07 | Subscribe → viewer-relative following true | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-08 | Unsubscribe → following false | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-09 | Persist subscription edges across unseat/reseat | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-10 | Refuse self-subscribe | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-11 | Deny subscribe/unsubscribe while unseated | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-12 | Refuse missing/unknown author subscribe | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-13 | Empty subscription stream valid (not global fill) | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-14 | Guest public discovery after member unseats | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-15 | Subscription stream ⊆ subscribed authors’ published articles | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-16 | Unsubscribe removes author’s articles from stream | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-17 | Publish-in to subscribers’ streams on re-open | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-18 | Delete-out from subscribers’ streams on re-open | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-19 | Subscription stream private to subscriber | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-20 | Tag lanes stay tag-true under subscription churn | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-21 | Newest-first global listing and subscription stream | `docs/specification/product/INIT-REALWORLD-002-api.md` | W1 |
| REQ-22 | Omit seated-only `following` for Guest profile reads | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |
| REQ-23 | Already-subscribed subscribe remains subscribed (no distinct error) | `docs/specification/product/INIT-REALWORLD-002-api.md` | W0 |

---

## 2. Implementation phases

### Phase W0 — Subscription wire + stewardship denials + CAP-02/03 prove

**GOAL-W0:** Land ADR-005 idempotent same-state subscribe and ADR-006 Guest `following` omit; harden self/missing/unseated denials, empty-stream validity, and reseat persistence; co-ship `make check`, live verify drivers, and fixtures for CAP-02/CAP-03.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W0-01 | Add Makefile `check` target and `tests/README.md` feature map pointing at live modules (not coverage SSOT) | REQ-07 | — | `Makefile` modify; `tests/README.md` create | `make check` exits 0 on clean tree | command / `make check` | exit 0 | Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `make check` | python-tooling incremental | ADR-001 | feature/INIT-REALWORLD-002-w0-subscription-wire |
| TASK-W0-02 | Same-state subscribe returns HTTP 200 + `following: true` without write; invert duplicate-subscribe unit; keep same-state unsubscribe HTTP 400 | REQ-07, REQ-08, REQ-23 | TASK-W0-01 | `app/api/routes/profiles.py` modify; `tests/test_api/test_routes/test_profiles.py` modify | Duplicate POST follow → 200 + following true; graph unchanged; DELETE when not following → 400 | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; assertions green | Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | ADR-005; TDD FF-01b | feature/INIT-REALWORLD-002-w0-subscription-wire |
| TASK-W0-03 | Guest profile (and embedded author) omits `following` key; seated responses keep boolean; invert guest unit | REQ-04, REQ-22 | TASK-W0-02 | `app/models/domain/profiles.py` modify; `app/models/schemas/profiles.py` modify; `app/db/repositories/profiles.py` modify; `tests/test_api/test_routes/test_profiles.py` modify; `tests/test_api/test_routes/test_articles.py` modify | Guest profile JSON lacks `following`; seated true/false still present; public reads stay ungated | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; key-absence assertions | Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | pydantic-schemas under ADR-001 | ADR-006 | feature/INIT-REALWORLD-002-w0-subscription-wire |
| TASK-W0-04 | Harden self/missing/unseated denials; empty feed not global; reseat persistence coverage | REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14 | TASK-W0-03 | `app/api/routes/profiles.py` modify; `tests/test_api/test_routes/test_profiles.py` modify; `tests/test_api/test_routes/test_articles.py` modify | Self-subscribe 400; missing author 404; unseated mutate 401; empty feed `[]` ≠ global membership; edges survive JWT discard + re-login | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; denial + empty + reseat assertions | Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-04 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | ADR-004 | feature/INIT-REALWORLD-002-w0-subscription-wire |
| TASK-W0-05 | Co-ship CAP-02/CAP-03 live verify + fixtures with `prayog:covers` | REQ-04, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-22, REQ-23 | TASK-W0-04 | `tests/verify/__init__.py` create; `tests/verify/verify_wave0_subscription_stewardship.py` create; `tests/fixtures/cap-02-subscription/stimulus.json` create; `tests/fixtures/cap-02-subscription/expected.json` create; `tests/fixtures/cap-02-subscription/cleanup.md` create; `tests/fixtures/cap-03-denial-empty/stimulus.json` create; `tests/fixtures/cap-03-denial-empty/expected.json` create; `tests/fixtures/cap-03-denial-empty/cleanup.md` create; `tests/fixtures/j-04-subscribe-cycle/stimulus.json` create; `tests/fixtures/j-08-empty-stream/stimulus.json` create; `tests/fixtures/j-10-unseat-deny/stimulus.json` create; `tests/fixtures/j-13-reseat-persist/stimulus.json` create | Script declares `prayog:covers:` including CAP-02, CAP-03, J-04, J-07, J-08, J-10, J-12, J-13; exits 0 against local compose | command / `poetry run python -m tests.verify.verify_wave0_subscription_stewardship` | exit 0; PASS markers | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run python -m tests.verify.verify_wave0_subscription_stewardship` | testing-verify-flows | ADR-001/004/005/006 | feature/INIT-REALWORLD-002-w0-subscription-wire |

#### Files (W0)

| ID | Path | Action |
|----|------|--------|
| FILE-W0-01 | `Makefile` | modify |
| FILE-W0-02 | `tests/README.md` | create |
| FILE-W0-03 | `app/api/routes/profiles.py` | modify |
| FILE-W0-04 | `app/models/domain/profiles.py` | modify |
| FILE-W0-05 | `app/models/schemas/profiles.py` | modify |
| FILE-W0-06 | `app/db/repositories/profiles.py` | modify |
| FILE-W0-07 | `tests/test_api/test_routes/test_profiles.py` | modify |
| FILE-W0-08 | `tests/test_api/test_routes/test_articles.py` | modify |
| FILE-W0-09 | `tests/verify/__init__.py` | create |
| FILE-W0-10 | `tests/verify/verify_wave0_subscription_stewardship.py` | create |
| FILE-W0-11 | `tests/fixtures/cap-02-subscription/stimulus.json` | create |
| FILE-W0-12 | `tests/fixtures/cap-02-subscription/expected.json` | create |
| FILE-W0-13 | `tests/fixtures/cap-02-subscription/cleanup.md` | create |
| FILE-W0-14 | `tests/fixtures/cap-03-denial-empty/stimulus.json` | create |
| FILE-W0-15 | `tests/fixtures/cap-03-denial-empty/expected.json` | create |
| FILE-W0-16 | `tests/fixtures/cap-03-denial-empty/cleanup.md` | create |
| FILE-W0-17 | `tests/fixtures/j-04-subscribe-cycle/stimulus.json` | create |
| FILE-W0-18 | `tests/fixtures/j-08-empty-stream/stimulus.json` | create |
| FILE-W0-19 | `tests/fixtures/j-10-unseat-deny/stimulus.json` | create |
| FILE-W0-20 | `tests/fixtures/j-13-reseat-persist/stimulus.json` | create |

#### Tests (W0)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W0-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-07..14, REQ-22, REQ-23 / TASK-W0-02..04 |
| TEST-W0-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres via existing async fixtures — boundary: asyncpg / followers table) | REQ-07..13, REQ-22, REQ-23 |
| TEST-W0-L | live (smoke) | `poetry run python -m tests.verify.verify_wave0_subscription_stewardship` | CAP-02, CAP-03 / J-04, J-07, J-08, J-09, J-10, J-12, J-13 |

#### Verification Coverage (W0)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-07/08/23 subscribe stewardship | CAP-02 / J-04 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | ADR-005 |
| REQ-09 reseat persistence | CAP-02 / J-13 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | ADR-004 |
| REQ-10/11/12 denials | CAP-03 / J-07,J-10,J-12 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-13 empty stream | CAP-03 / J-08 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | not global fill |
| REQ-04/14/22 guest wire | CAP-01/CAP-02 / J-09,J-10 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | ADR-006 |

#### Live-verification intent (W0)

| Field | Value |
|-------|-------|
| Applicable | yes — new product surface + new `tests/verify` |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-02, CAP-03 / J-04, J-07, J-08, J-09, J-10, J-12, J-13 |
| Fixture packs | `tests/fixtures/cap-02-subscription/`, `tests/fixtures/cap-03-denial-empty/`, `tests/fixtures/j-04-subscribe-cycle/`, `tests/fixtures/j-08-empty-stream/`, `tests/fixtures/j-10-unseat-deny/`, `tests/fixtures/j-13-reseat-persist/` |
| Runtime head binding | Bound at `wave-acceptance` against the wave PR head under test (not filled at planning) |
| Prerequisites / dependencies | Postgres up; API reachable via realworld-local compose |
| Safe test data | Synthetic users/edges only — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave0_subscription_stewardship` |
| Expected observations | Script exit 0; subscribe/unsubscribe polarity PASS; Guest omits `following`; empty feed not global; unseated mutate 401; reseat keeps edges |
| Human look-ats | API JSON for duplicate POST follow → 200 + following true; Guest profile key absence; empty `/articles/feed` vs populated `/articles` |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic users/edges per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

### Phase W1 — Discovery continuity + newest-first + stream lifecycle + CAP-01/04 prove

**GOAL-W1:** Implement REQ-21 newest-first ordering on global listing and subscription stream; add unfollow/publish-in/delete-out stream lifecycle units; keep public/tag membership subscription-independent; co-ship CAP-01/CAP-04 live prove; seed as-built detail + index pointer.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W1-01 | Global/tag/author listing ORDER BY `updated_at DESC, created_at DESC`; unit order assertions | REQ-01, REQ-02, REQ-03, REQ-06, REQ-21 | — | `app/db/repositories/articles.py` modify; `tests/test_api/test_routes/test_articles.py` modify; `tests/test_api/test_routes/test_tags.py` modify | ≥2 seeded articles return newest-first; Guest list/get/tag remain ungated | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; order assertions | Wave-Execution-INIT-REALWORLD-002-W1.md § TASK-W1-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | repository-pattern | TDD FF-04 | feature/INIT-REALWORLD-002-w1-discovery-stream |
| TASK-W1-02 | Feed SQL same DESC pair; stream ⊆ followed authors; unfollow/publish/delete lifecycle; unauth feed 401 | REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-21 | TASK-W1-01 | `app/db/queries/sql/articles.sql` modify; `app/api/routes/articles/articles_common.py` modify; `tests/test_api/test_routes/test_articles.py` modify | Feed newest-first; unfollow removes; publish-in/delete-out on re-open; no peer public stream | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; lifecycle assertions | Wave-Execution-INIT-REALWORLD-002-W1.md § TASK-W1-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | TDD FF-05/FF-06 | feature/INIT-REALWORLD-002-w1-discovery-stream |
| TASK-W1-03 | Public listing + tag lanes unchanged by subscribe/unsubscribe churn; no ∩ surface | REQ-04, REQ-05, REQ-06, REQ-20 | TASK-W1-02 | `tests/test_api/test_routes/test_articles.py` modify; `tests/test_api/test_routes/test_tags.py` modify | Membership sets identical before/after subscription churn for global + tag lane | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; membership assertions | Wave-Execution-INIT-REALWORLD-002-W1.md § TASK-W1-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | — | feature/INIT-REALWORLD-002-w1-discovery-stream |
| TASK-W1-04 | Co-ship CAP-01/CAP-04 live verify + fixtures; seed as-built detail + index pointer | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21 | TASK-W1-03 | `tests/verify/verify_wave1_discovery_stream.py` create; `tests/fixtures/cap-01-discovery/stimulus.json` create; `tests/fixtures/cap-01-discovery/expected.json` create; `tests/fixtures/cap-01-discovery/cleanup.md` create; `tests/fixtures/cap-04-stream/stimulus.json` create; `tests/fixtures/cap-04-stream/expected.json` create; `tests/fixtures/cap-04-stream/cleanup.md` create; `tests/fixtures/j-01-guest-discovery/stimulus.json` create; `tests/fixtures/j-05-stream-read/stimulus.json` create; `tests/fixtures/j-06-unfollow-stream/stimulus.json` create; `tests/fixtures/j-11-publish-in/stimulus.json` create; `tests/fixtures/j-14-tag-churn/stimulus.json` create; `tests/fixtures/j-15-stream-privacy/stimulus.json` create; `tests/fixtures/j-16-delete-out/stimulus.json` create; `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-002.md` create; `docs/specification/as-built/implementation-status.md` create; `tests/README.md` modify | Live verify exits 0 with CAP-01/CAP-04 covers; as-built detail + index pointer exist | command / `poetry run python -m tests.verify.verify_wave1_discovery_stream` | exit 0; as-built files present | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-002-api.md` | `poetry run python -m tests.verify.verify_wave1_discovery_stream` | testing-verify-flows; SDD as-built | ADR-001 | feature/INIT-REALWORLD-002-w1-discovery-stream |

#### Files (W1)

| ID | Path | Action |
|----|------|--------|
| FILE-W1-01 | `app/db/repositories/articles.py` | modify |
| FILE-W1-02 | `app/db/queries/sql/articles.sql` | modify |
| FILE-W1-03 | `app/api/routes/articles/articles_common.py` | modify |
| FILE-W1-04 | `tests/test_api/test_routes/test_articles.py` | modify |
| FILE-W1-05 | `tests/test_api/test_routes/test_tags.py` | modify |
| FILE-W1-06 | `tests/verify/verify_wave1_discovery_stream.py` | create |
| FILE-W1-07 | `tests/fixtures/cap-01-discovery/stimulus.json` | create |
| FILE-W1-08 | `tests/fixtures/cap-01-discovery/expected.json` | create |
| FILE-W1-09 | `tests/fixtures/cap-01-discovery/cleanup.md` | create |
| FILE-W1-10 | `tests/fixtures/cap-04-stream/stimulus.json` | create |
| FILE-W1-11 | `tests/fixtures/cap-04-stream/expected.json` | create |
| FILE-W1-12 | `tests/fixtures/cap-04-stream/cleanup.md` | create |
| FILE-W1-13 | `tests/fixtures/j-01-guest-discovery/stimulus.json` | create |
| FILE-W1-14 | `tests/fixtures/j-05-stream-read/stimulus.json` | create |
| FILE-W1-15 | `tests/fixtures/j-06-unfollow-stream/stimulus.json` | create |
| FILE-W1-16 | `tests/fixtures/j-11-publish-in/stimulus.json` | create |
| FILE-W1-17 | `tests/fixtures/j-14-tag-churn/stimulus.json` | create |
| FILE-W1-18 | `tests/fixtures/j-15-stream-privacy/stimulus.json` | create |
| FILE-W1-19 | `tests/fixtures/j-16-delete-out/stimulus.json` | create |
| FILE-W1-20 | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-002.md` | create |
| FILE-W1-21 | `docs/specification/as-built/implementation-status.md` | create |
| FILE-W1-22 | `tests/README.md` | modify |

#### Tests (W1)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W1-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-15..21 / TASK-W1-01..03 |
| TEST-W1-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres — boundary: article timestamps + followers join) | REQ-01..06, REQ-15..21 |
| TEST-W1-L | live (smoke) | `poetry run python -m tests.verify.verify_wave1_discovery_stream` | CAP-01, CAP-04 / J-01, J-02, J-03, J-05, J-06, J-11, J-14, J-15, J-16 |

#### Verification Coverage (W1)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-01..06 discovery continuity | CAP-01 / J-01,J-02,J-03,J-14 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-15..19 stream honesty/privacy | CAP-04 / J-05,J-06,J-11,J-15,J-16 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-20 tag-true under churn | CAP-04 / J-14 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-21 newest-first | CAP-01/CAP-04 / J-03,J-05 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | FF-04/FF-05 |

#### Live-verification intent (W1)

| Field | Value |
|-------|-------|
| Applicable | yes — material CAP-01/CAP-04 surface + new live module |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-01, CAP-04 / J-01, J-02, J-03, J-05, J-06, J-11, J-14, J-15, J-16 |
| Fixture packs | `tests/fixtures/cap-01-discovery/`, `tests/fixtures/cap-04-stream/`, journey packs `j-01`..`j-16` listed in Files |
| Runtime head binding | Bound at `wave-acceptance` (not planning) |
| Prerequisites / dependencies | W0 green; Postgres up; API via realworld-local compose |
| Safe test data | Synthetic authors/articles/tags/edges — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave1_discovery_stream` |
| Expected observations | Guest discovery ungated; stream ⊆ followed; unfollow/publish/delete lifecycle; tag membership unchanged by churn; newest-first order |
| Human look-ats | Feed vs global membership sets; slug order for seeded timestamps; Guest 401 on `/articles/feed` |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic data per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

## 3. Dependencies (DEP)

| ID | Dependency | Blocks |
|----|------------|--------|
| DEP-01 | W0 subscription wire + CAP-02/03 prove | W1 discovery/stream prove (depends on honest follow graph + Guest omit) |
| DEP-02 | `realworld-local` compose up for live smoke | W0/W1 wave-acceptance human prove |
| DEP-03 | INIT-REALWORLD-001 seat/bulletin baseline in force (not reopened) | All CAP-01..04 REQs |
| DEP-04 | Accepted ADR-001 (`app/` chassis) | All code TASKs |
| DEP-05 | Accepted ADR-005 / ADR-006 | TASK-W0-02 / TASK-W0-03 |

---

## 4. Risks (RISK)

| ID | Risk | Mitigation |
|----|------|------------|
| RISK-01 | Consumer (web) still expects Conduit 400 on duplicate follow POST | ADR-005 locked; CTR-02 verify asserts 200; coordinate web UAT language |
| RISK-02 | Guest clients break on missing `following` key | ADR-006; OpenAPI/examples; live J-09 look-at |
| RISK-03 | Feed/global ordering drift if only one surface fixed | W1 tasks cover both `filter_articles` and `get-articles-for-feed` |
| RISK-04 | As-built absent → false “live” maturity claims | Seed as-built in W1 same PR as CAP-01/04 prove (P9) |
| RISK-05 | Chassis/MDC tension (`src/` vs `app/`) | Cite Accepted ADR-001; no INIT-002 migrate |
| RISK-06 | Mid-view empty/delete chrome without re-open (Q-06/Q-11) | Deferred; API next-open sufficient per defaults |

---

## 5. Out of scope

- `realworld-web` UAT chrome / kill-path driving
- `realworld-local` compose product CAP ownership beyond prove environment
- Follower/following **counts** (IM-01 / OQ-01 deferred)
- Comments, OAuth, email verification, mobile/native clients
- Reopening INIT-REALWORLD-001 favorites/nameplate rules
- Composed subscription∩tag discovery surface
- Mutual-friends packaging
- Idempotent same-state **unsubscribe** success (TDD FF-01b retains HTTP 400)
- Mid-view push without re-open (IM-06 / IM-11)
- Platform `src/` migrate (ADR-001)

---

## 6. As-built and docs tasks

> Update these in the **same PR** as the code they describe.

| Task | File | Action |
|------|------|--------|
| Create/update per-initiative as-built detail | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-002.md` | Record W1 capability/code/test/verify detail — **KEEP** |
| Update as-built index row | `docs/specification/as-built/implementation-status.md` | Overwrite this capability’s one row in place (pointer) — never append a new table |
| Ensure live-verify coverage marker | `tests/verify/verify_wave0_subscription_stewardship.py` / `tests/verify/verify_wave1_discovery_stream.py` | Self-declare `prayog:covers:` — **do not** treat `tests/README.md` as coverage SSOT |

> **ADR lifecycle** — Draft and Accepted ADR files are created and accepted during
> `/spec-technical-review` and the `technical-review-approval` checkpoint.
> Planning consumes Accepted files only; do not add ADR promotion tasks here.

---

## 7. Plan check summary

| Check | Status |
|-------|--------|
| P1 | PASS — REQ-01..23 in §1; each wave cites via TASK Implements |
| P2 | PASS — every REQ has ≥1 TASK; every TASK Implements ≥1 REQ-* |
| P3 | PASS — every TASK has FILE paths |
| P4 | PASS — observable exit criteria + proof + expected + evidence_expected |
| P5 | PASS — unit / integration(Postgres) / smoke layers; Verification Coverage tables |
| P6 | PASS — scope bounded to INIT-002-api provider REQs |
| P7 | PASS — FF-01..07 addressed in TDD/ADR/plan; Q-06/07/11 deferred with owner+default |
| P8 | PASS — W0 → W1; DEP table |
| P9 | PASS — as-built detail + index in W1 FILE list |
| P10 | PASS — self-contained; digests; commands; live prerequisites |
| P11 | PASS — MDC notes; ADR-001 chassis exception |
| P12 | PASS — ADR-005/006 Accepted + cited; ADR-001/004 constraining |
| P13 | PASS — TDD Accepted; PE sign-off complete; product-boundary false; plan-time lint PASS |
| P14 | PASS — §9 WorkManifest present; W0/W1; tasks[] + body tables |
| P15 | PASS — overlap check recorded (verify dir absent → new FILEs); unit+live+fixtures co-shipped; covers include CAP/J |
| P16 | PASS — `python prayog-skills/scripts/workmanifest_contract.py` exit 0 on this plan |

---

## 8. Forge / PR instructions

> Persist this plan locally and publish via `/commit-workspace` (or Gateflow
> ForgeClient) to the **Draft spec PR** branch alongside spec, feasibility,
> and TDD. Do **not** commit inside this skill. Label remains **`spec-pending`**
> until PE completes §10.

```
Branch:   docs/spec-init-realworld-002  (Draft PR)
PR title: "[INIT-REALWORLD-002] Spec — realworld-api"
PR body:  link meta PRD PR #8; paste §1 Requirements table + wave goals summary

Required reviewers: @drivestream-lab/backend-devs
Review deadline: 2026-11-17

PE checklist (before spec-lgtm):
  [ ] Spec + feasibility + TDD + Accepted ADRs + this plan on current head
  [ ] §0 PE sign-off on TDD marked complete — required, no N/A path
  [ ] Wave order and dependencies make sense
  [ ] Done-when / exit criteria are observable and testable (P4)
  [ ] Verification Coverage maps every criterion to a layer (P5)
  [ ] WorkManifest YAML (§9) passes workmanifest-contract-pass (P16) — prayog/v1
  [ ] P1–P16 checks all pass (including P15 co-ship when surface changes)

After spec-lgtm + Approve + merge — **`/create-board-tickets`** from §9 (post-merge only):
  Create one GitHub Issue per wave (W0, W1) using §9 titles, bodies, depends_on
  Search for existing initiative/wave issues first; create only missing issues
  Then Pass-1: /pre-implement → /loop-spec → wave-acceptance (human runs co-shipped script)
  Then Pass-2: /learning-extract → /ground-spec → wave-signoff (merge only)
```

---

## 10. Coding-readiness unlock (PE — after plan on head)

| Item | Value |
|------|-------|
| Workflow outcome | `pass` — P1–P16 PASS; sources CURRENT; Accepted TDD/ADRs; plan ready for coding-readiness |
| Verdict | GATE OPEN REQUEST |
| Spec PR | https://github.com/drivestream-lab/realworld-api/pull/11 |
| Spec PR head SHA | `93cedca068c2940e034d06d6b1ba24bcfbc3beda` (pre-Forge; PE must attest exact head after `/commit-workspace`) |
| Gate label (current) | `spec-pending` |
| Gate label (target) | `spec-lgtm` |
| Local plan path | `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-002.md` |
| Forge readiness | fill `handoff.forge` for `/commit-workspace` — do not commit inside this skill |
| Blocking items | none |

Provision labels when missing:

```bash
launchpad apply-gates --repo realworld-api --apply
```

PE actions (all on **exact current head**):

1. Remove `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale`; add **`spec-lgtm`**
2. Submit GitHub **Approve** with attestation body (below)
3. Mark Draft PR **Ready for review**
4. Authorize merge (human or policy); then **`/create-board-tickets`** from §9

### Approve attestation body

```text
Spec package approved
initiative: INIT-REALWORLD-002
spec_pr_head_sha: {SHA after Forge publish}
meta_pr_head_sha: ee9fe45ad23d988eface7517a3a65a7b58b592c1
impact_map_revision: 1
prd_digest: sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92
scope_digest: sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0
plan_digest: sha256:04c30dbb82e963a748234bdcd202c1b610903082bddaae4f24a72a3fb9190c02
artifacts:
  - docs/specification/product/INIT-REALWORLD-002-api.md
  - docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-002.md
  - docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md
  - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-002.md
```

Never infer approval from `spec-lgtm` alone — Approve, label, and artifact
digests must match the same head SHA.

| PE action | Remove | Add |
|-----------|--------|-----|
| Pending/new revision | `spec-lgtm`, `spec-blocked` | `spec-pending` |
| Request changes/hold | `spec-pending`, `spec-lgtm` | `spec-blocked` |
| Approve full package | `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale` | `spec-lgtm` |

---

## 9. WorkManifest seed

> **Primary:** `/create-board-tickets` creates **one GitHub Issue per wave** (`W0`, `W1`)
> from this section after spec merge. Wave bodies **must list every `TASK-*`**
> with exit criteria for human traceability (TASK sub-issues optional).
>
> Contract: `prayog-skills/references/workmanifest-contract.md` (`prayog/v1`).
> Validate: `python prayog-skills/scripts/workmanifest_contract.py` on this plan.
> `target.org` / `target.project` from governance (`RealWorld`).

```yaml
# Generated by /spec-implementation-plan — 2026-11-12
# LOCAL — do not commit to prayog-skills upstream
apiVersion: prayog/v1
kind: WorkManifest

initiative: INIT-REALWORLD-002
metadata:
  title: INIT-REALWORLD-002 — Author-subscription trust with denial-honest empties
  summary: |
    Provider plan for CAP-01..CAP-04: ADR-005/006 subscription wire, denial-honest
    empties, newest-first listing/stream, and subscription-stream lifecycle honesty
    under the Accepted ADR-001 app/ chassis, with co-shipped live prove.
  playbook:
    - docs/specification/product/INIT-REALWORLD-002-api.md
    - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-002.md

target:
  org: drivestream-lab
  project: RealWorld

defaults:
  initiative: INIT-REALWORLD-002
  parent: EPIC
  labels:
    - INIT-REALWORLD-002

epic:
  id: EPIC
  repo: realworld-api
  title: "[feature] INIT-REALWORLD-002 — Author-subscription trust with denial-honest empties"
  codebase: realworld-api
  spec_path: docs/specification/product/INIT-REALWORLD-002-api.md
  verify_command: poetry run python -m tests.verify.verify_wave1_discovery_stream
  body: |
    ## Objective

    Make author subscription trustworthy on realworld-api: seated subscribe/unsubscribe
    with viewer-relative state, denial-honest empties, and a subscription stream that
    honestly projects current edges — while public discovery stays ungated and unpersonalized.

    ## Waves

    | Wave | Goal |
    |------|------|
    | W0 | Subscription wire + stewardship denials + CAP-02/03 prove |
    | W1 | Discovery continuity + newest-first + stream lifecycle + CAP-01/04 prove |

    ## References

    - Spec: docs/specification/product/INIT-REALWORLD-002-api.md
    - Implementation plan: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-002.md
    - Technical review: docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md

work:
  - id: W0
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-002 W0] Subscription wire + stewardship denials + CAP-02/03 prove"
    depends_on: []
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-002-api.md
    verify_command: poetry run python -m tests.verify.verify_wave0_subscription_stewardship
    tasks:
      - id: TASK-W0-01
        implements: [REQ-07]
        depends_on: []
        files:
          - path: Makefile
            action: modify
          - path: tests/README.md
            action: create
        exit:
          criteria:
            - "make check exits 0 on a clean tree after the check target is added"
          proof:
            kind: command
            command: make check
            expected: "exit 0"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-01"
      - id: TASK-W0-02
        implements: [REQ-07, REQ-08, REQ-23]
        depends_on: [TASK-W0-01]
        files:
          - path: app/api/routes/profiles.py
            action: modify
          - path: tests/test_api/test_routes/test_profiles.py
            action: modify
        exit:
          criteria:
            - "Duplicate subscribe POST returns HTTP 200 with following true and unchanged graph; same-state unsubscribe remains HTTP 400"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; duplicate-subscribe and unsubscribe polarity assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-02"
      - id: TASK-W0-03
        implements: [REQ-04, REQ-22]
        depends_on: [TASK-W0-02]
        files:
          - path: app/models/domain/profiles.py
            action: modify
          - path: app/models/schemas/profiles.py
            action: modify
          - path: app/db/repositories/profiles.py
            action: modify
          - path: tests/test_api/test_routes/test_profiles.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
        exit:
          criteria:
            - "Guest profile JSON omits the following key; seated responses keep the boolean; public reads remain ungated"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; Guest key-absence assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-03"
      - id: TASK-W0-04
        implements: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14]
        depends_on: [TASK-W0-03]
        files:
          - path: app/api/routes/profiles.py
            action: modify
          - path: tests/test_api/test_routes/test_profiles.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
        exit:
          criteria:
            - "Self-subscribe and missing-author fail closed; unseated mutate denied; empty feed is not global membership; edges survive JWT discard and re-login"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; denial empty and reseat assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W0.md § TASK-W0-04"
      - id: TASK-W0-05
        implements: [REQ-04, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-22, REQ-23]
        depends_on: [TASK-W0-04]
        files:
          - path: tests/verify/__init__.py
            action: create
          - path: tests/verify/verify_wave0_subscription_stewardship.py
            action: create
          - path: tests/fixtures/cap-02-subscription/stimulus.json
            action: create
          - path: tests/fixtures/cap-02-subscription/expected.json
            action: create
          - path: tests/fixtures/cap-02-subscription/cleanup.md
            action: create
          - path: tests/fixtures/cap-03-denial-empty/stimulus.json
            action: create
          - path: tests/fixtures/cap-03-denial-empty/expected.json
            action: create
          - path: tests/fixtures/cap-03-denial-empty/cleanup.md
            action: create
          - path: tests/fixtures/j-04-subscribe-cycle/stimulus.json
            action: create
          - path: tests/fixtures/j-08-empty-stream/stimulus.json
            action: create
          - path: tests/fixtures/j-10-unseat-deny/stimulus.json
            action: create
          - path: tests/fixtures/j-13-reseat-persist/stimulus.json
            action: create
        exit:
          criteria:
            - "Live verify script exits 0 with prayog:covers including CAP-02 and CAP-03"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave0_subscription_stewardship
            expected: "exit 0; PASS markers for CAP-02/CAP-03"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave0_subscription_stewardship
        covers: [CAP-02, CAP-03, J-04, J-07, J-08, J-09, J-10, J-12, J-13, REQ-07, REQ-11, REQ-13, REQ-22, REQ-23]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-02-subscription/
          - tests/fixtures/cap-03-denial-empty/
          - tests/fixtures/j-04-subscribe-cycle/
          - tests/fixtures/j-08-empty-stream/
          - tests/fixtures/j-10-unseat-deny/
          - tests/fixtures/j-13-reseat-persist/
        prerequisites:
          - "compose up; synthetic users available"
        safe_test_data:
          - "synthetic users and follow edges — no prod mutation"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave0_subscription_stewardship"
        expected_observations:
          - "Subscribe cycle PASS; Guest omits following; empty feed not global; unseated mutate denied; reseat keeps edges"
        human_observations:
          - locus: "API JSON duplicate follow POST + Guest profile + empty feed vs global"
            expect: "200 following true; following key absent for Guest; feed [] while global may be non-empty"
            covers: [CAP-02, CAP-03]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic users/edges per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Subscription wire + stewardship denials + CAP-02/03 prove

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W0-01 | REQ-07 | — | make check exits 0 | command/make check |
      | TASK-W0-02 | REQ-07, REQ-08, REQ-23 | TASK-W0-01 | idempotent subscribe wire | command/pytest |
      | TASK-W0-03 | REQ-04, REQ-22 | TASK-W0-02 | Guest omit following | command/pytest |
      | TASK-W0-04 | REQ-09..14 | TASK-W0-03 | denials + empty + reseat | command/pytest |
      | TASK-W0-05 | REQ-04,07..14,22,23 | TASK-W0-04 | live CAP-02/CAP-03 | command/verify_wave0 |

      ## Done when

      - [ ] All W0 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-002-api.md

  - id: W1
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-002 W1] Discovery continuity + newest-first + stream lifecycle + CAP-01/04 prove"
    depends_on:
      - W0
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-002-api.md
    verify_command: poetry run python -m tests.verify.verify_wave1_discovery_stream
    tasks:
      - id: TASK-W1-01
        implements: [REQ-01, REQ-02, REQ-03, REQ-06, REQ-21]
        depends_on: []
        files:
          - path: app/db/repositories/articles.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
          - path: tests/test_api/test_routes/test_tags.py
            action: modify
        exit:
          criteria:
            - "Global and tag listings return newest-first by updated_at then created_at for seeded articles; Guest reads remain ungated"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; order and ungated assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W1.md § TASK-W1-01"
      - id: TASK-W1-02
        implements: [REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-21]
        depends_on: [TASK-W1-01]
        files:
          - path: app/db/queries/sql/articles.sql
            action: modify
          - path: app/api/routes/articles/articles_common.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
        exit:
          criteria:
            - "Feed orders newest-first; unfollow/publish-in/delete-out change stream membership on re-open; unauthenticated feed is denied"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; lifecycle and privacy assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W1.md § TASK-W1-02"
      - id: TASK-W1-03
        implements: [REQ-04, REQ-05, REQ-06, REQ-20]
        depends_on: [TASK-W1-02]
        files:
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
          - path: tests/test_api/test_routes/test_tags.py
            action: modify
        exit:
          criteria:
            - "Global and tag-lane membership sets are unchanged by subscribe/unsubscribe churn alone"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; membership-independence assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-002-W1.md § TASK-W1-03"
      - id: TASK-W1-04
        implements: [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21]
        depends_on: [TASK-W1-03]
        files:
          - path: tests/verify/verify_wave1_discovery_stream.py
            action: create
          - path: tests/fixtures/cap-01-discovery/stimulus.json
            action: create
          - path: tests/fixtures/cap-01-discovery/expected.json
            action: create
          - path: tests/fixtures/cap-01-discovery/cleanup.md
            action: create
          - path: tests/fixtures/cap-04-stream/stimulus.json
            action: create
          - path: tests/fixtures/cap-04-stream/expected.json
            action: create
          - path: tests/fixtures/cap-04-stream/cleanup.md
            action: create
          - path: tests/fixtures/j-01-guest-discovery/stimulus.json
            action: create
          - path: tests/fixtures/j-05-stream-read/stimulus.json
            action: create
          - path: tests/fixtures/j-06-unfollow-stream/stimulus.json
            action: create
          - path: tests/fixtures/j-11-publish-in/stimulus.json
            action: create
          - path: tests/fixtures/j-14-tag-churn/stimulus.json
            action: create
          - path: tests/fixtures/j-15-stream-privacy/stimulus.json
            action: create
          - path: tests/fixtures/j-16-delete-out/stimulus.json
            action: create
          - path: docs/specification/as-built/Implementation-Status-INIT-REALWORLD-002.md
            action: create
          - path: docs/specification/as-built/implementation-status.md
            action: create
          - path: tests/README.md
            action: modify
        exit:
          criteria:
            - "Live verify exits 0 with CAP-01 and CAP-04 covers; as-built detail and index pointer files exist"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave1_discovery_stream
            expected: "exit 0; as-built files present"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave1_discovery_stream
        covers: [CAP-01, CAP-04, J-01, J-02, J-03, J-05, J-06, J-11, J-14, J-15, J-16, REQ-01, REQ-15, REQ-20, REQ-21]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-01-discovery/
          - tests/fixtures/cap-04-stream/
          - tests/fixtures/j-01-guest-discovery/
          - tests/fixtures/j-05-stream-read/
          - tests/fixtures/j-06-unfollow-stream/
          - tests/fixtures/j-11-publish-in/
          - tests/fixtures/j-14-tag-churn/
          - tests/fixtures/j-15-stream-privacy/
          - tests/fixtures/j-16-delete-out/
        prerequisites:
          - "W0 green; compose up; multi-author synthetic corpus"
        safe_test_data:
          - "synthetic authors/articles/tags/edges — no prod mutation"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave1_discovery_stream"
        expected_observations:
          - "Guest discovery ungated; stream lifecycle honest; tag lanes unchanged by churn; newest-first order"
        human_observations:
          - locus: "Guest /articles vs /articles/feed membership and slug order"
            expect: "feed subset of followed authors; order newest-first; Guest feed 401"
            covers: [CAP-01, CAP-04]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic data per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Discovery continuity + newest-first + stream lifecycle + CAP-01/04 prove

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W1-01 | REQ-01,02,03,06,21 | — | global newest-first | command/pytest |
      | TASK-W1-02 | REQ-15..19,21 | TASK-W1-01 | stream lifecycle | command/pytest |
      | TASK-W1-03 | REQ-04,05,06,20 | TASK-W1-02 | tag/global independence | command/pytest |
      | TASK-W1-04 | REQ-01..06,15..21 | TASK-W1-03 | live CAP-01/04 + as-built | command/verify_wave1 |

      ## Done when

      - [ ] All W1 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-002-api.md
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-implementation-plan
  outcome: pass
  artifact:
    path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-002.md
    digest: sha256:04c30dbb82e963a748234bdcd202c1b610903082bddaae4f24a72a3fb9190c02
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92
    scope_digest: sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0
    meta_pr_approved_head: ee9fe45ad23d988eface7517a3a65a7b58b592c1
    draft_spec_pr: https://github.com/drivestream-lab/realworld-api/pull/11
    workmanifest_contract: pass
    p15_overlap: tests/verify absent — new FILEs warranted
    codegraph_provider: degraded-none
    grounding_depth: deep
    plan_status: Planned
    adr_lint:
      - "ADR-005 Lint evidence: adr_boundary_lint.py 5/5, PASS, sha256:7fc921cfa52e6cf035acfa44fbfa27da9bb0a527e953a9d9c157916196f67dfa"
      - "ADR-006 Lint evidence: adr_boundary_lint.py 5/5, PASS, sha256:bf81fe7fc238bc8c595ebff37167b76b65e6b830b1d7aebd770cee9b703b17d4"
  next_candidates:
    - coding-readiness
  human_checkpoint: true
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-002] Spec — realworld-api (implementation plan)"
    body_path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-002.md
    target_branch: docs/spec-init-realworld-002
```
