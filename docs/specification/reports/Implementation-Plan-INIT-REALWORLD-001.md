---
goal: INIT-REALWORLD-001 — implementation plan
initiative: INIT-REALWORLD-001
status: Planned
date_created: 2026-11-11
source_spec: docs/specification/product/INIT-REALWORLD-001-api.md
feasibility_report: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md
technical_review: docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md
prd_digest: sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4
impact_map: realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-001.md
impact_map_revision: 1
repo_scope_digest: sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d
approved_meta_pr_head: a500df8eeefbea095ecdd65e00edb128416c3cf4
branch: docs/spec-init-realworld-001
review_deadline: 2026-11-16
deciders: PE — spec-lgtm + Approve on exact head after full package
---

# Implementation plan — INIT-REALWORLD-001

## Source freshness and command contract

| Item | Value | Status |
|------|-------|--------|
| Spec | `docs/specification/product/INIT-REALWORLD-001-api.md` | CURRENT — digest `sha256:006eb93a2b6006b9a8c0c54772f85e9c12c4de67dee3210fb3da15760b5ea360` matches live file |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md` | CURRENT — cites same H1/H2/H3/G1 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md` | CURRENT — `Status: Accepted`; §13 ready_for_plan=YES; ADR-001..004 Accepted |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-001.md` / `1` | CURRENT |
| Repo scope digest | `sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d` | CURRENT |
| Approved meta PR head | `a500df8eeefbea095ecdd65e00edb128416c3cf4` | CURRENT — meta PR #5 |
| `check_command` | `make check` | RESOLVED — W0 co-ships Makefile `check` target (`poetry run black --check app tests`); ADR-001 allows incremental tooling vs full pyright/import-linter |
| `test_command` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | RESOLVED |
| `verify_command` | Wave-scoped live modules under `tests/verify/` (W0 `poetry run python -m tests.verify.verify_wave0_seat_bulletin`; W1 `poetry run python -m tests.verify.verify_wave1_publish_revise`; W2 `poetry run python -m tests.verify.verify_wave2_shelf_nameplate`) | RESOLVED — co-shipped with product surface (P15); not unit |
| `ground_command` | N/A — as-built seeded in W2; `/ground-spec` after wave-acceptance (AF-2) | N/A — reason recorded |

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md` |
| Technical review status | Accepted |
| PE sign-off | [x] complete — 2026-11-11 (Buzz `accept tdd-adr` / god take on technical-review-approval) |
| Resolved ADRs | [`docs/specification/adr/adr-001-wave0a-package-chassis.md`](../adr/adr-001-wave0a-package-chassis.md) (Accepted); [`docs/specification/adr/adr-002-private-shelf-list-authorization.md`](../adr/adr-002-private-shelf-list-authorization.md) (Accepted); [`docs/specification/adr/adr-003-favorites-count-wire-policy.md`](../adr/adr-003-favorites-count-wire-policy.md) (Accepted); [`docs/specification/adr/adr-004-wave0a-unseat-token-discard.md`](../adr/adr-004-wave0a-unseat-token-discard.md) (Accepted) |
| ADR product-boundary re-check | All four: `changes_user_visible_behavior: false` / `spec_amendment_required: false`. Plan-time `adr_boundary_lint.py --strict --verify-lint-evidence` **PASS** on all four after Lint evidence refresh against `/tmp/init-rw001-t12` acceptance sources (`all-approved-reqs.txt` + `FF-NN-evidence.txt`) |
| Outstanding PM questions | none — all resolved |
| Outstanding domain questions | none — all resolved |

> Do not start W0 implementation until PE sign-off is marked complete above.

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | package chassis / `app/` vs `src/` | Accepted |
| ADR-002 | private-shelf `favorited=` authorization | Accepted |
| ADR-003 | `favoritesCount` wire policy | Accepted |
| ADR-004 | unseat via client JWT discard | Accepted |

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout / JWT / packages | read — Wave0a exception via Accepted ADR-001 |
| `fail-fast.mdc` | denial / no silent fallback | read |
| `http-api-conventions.mdc` | body/query/path | read |
| `repository-pattern.mdc` | repo boundary | read |
| `pydantic-schemas.mdc` | schemas | read |
| `testing-verify-flows.mdc` | verify vs pytest | read |
| `python-tooling.mdc` | make check | read — incremental `make check` in W0 |
| `dependency-injection.mdc` | injector | skipped — ADR-001 retains `app/` without injector migrate |
| `infra-services.mdc` | pools/clients | skipped — no new infra client |
| `logging-loguru.mdc` | logging | skipped — NFR observability N/A as kill criterion |
| others | — | skipped — not in Wave0a TASK touch set |

### P15 overlap check (recorded)

| Query | Result | Disposition |
|-------|--------|-------------|
| `PYTHONPATH=prayog-skills:. python3 prayog-skills/scripts/verify_coverage_query.py tests/verify --dump` | `error: not a directory: tests/verify` | **New** live verify FILEs warranted (AF-1) |
| `--capability CAP-01` .. `CAP-06` | same — dir absent | **New** fixture packs under `tests/fixtures/` warranted |

---

## 1. Requirements (REQ) — product ids

| ID | Summary | Spec path | Waves |
|----|---------|-----------|-------|
| REQ-01 | Guest global feed ungated | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-02 | Guest open article | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-03 | Guest tag lane | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-04 | Guest public profile + author articles | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-05 | Tag-hop discovery | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-06 | Multi-tag lane membership | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-07 | Reads after unseat | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-08 | Register eligibility (no seat JWT) | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-09 | Refuse duplicate register | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-10 | Login seats | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-11 | Invalid login refuse | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-12 | Logout unseat (client JWT discard) | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-13 | Reseat after re-login | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-14 | Unseated contribution deny | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-15 | Tagged publish visible | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-16 | Refuse zero-tag publish | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-17 | Bootstrap empty bulletin | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-18 | Refuse unseated publish | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-19 | No server draft on abandon | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-20 | Edit own article | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-21 | Tag-set lane consistency | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-22 | Refuse empty tag-set edit | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-23 | Delete own article | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-24 | Peer edit/delete deny | `docs/specification/product/INIT-REALWORLD-001-api.md` | W1 |
| REQ-25 | Favorite others → private shelf | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-26 | Unfavorite | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-27 | Shelf isolation across members | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-28 | Refuse own-article favorite | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-29 | Unseated favorite deny | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-30 | Nameplate bio/image; identity lock | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-31 | Peer nameplate deny | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-32 | Unseated nameplate deny | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-33 | No shelf resurrection after delete | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |
| REQ-34 | Newest-first feed order | `docs/specification/product/INIT-REALWORLD-001-api.md` | W0 |
| REQ-35 | Favorite missing/deleted fail-closed | `docs/specification/product/INIT-REALWORLD-001-api.md` | W2 |

---

## 2. Implementation phases

### Phase W0 — Seat + public bulletin + feed order + prove scaffold

**GOAL-W0:** Harden contribution-seat lifecycle (register eligibility without seat JWT; login seats; client JWT discard unseats per ADR-004) and ungated public bulletin reads with newest-first ordering (REQ-34); co-ship `make check`, live verify drivers, and fixtures for CAP-01/CAP-02.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W0-01 | Add Makefile `check` target and `tests/README.md` feature map pointing at live modules (not coverage SSOT) | REQ-01 | — | `Makefile` modify; `tests/README.md` create | `make check` exits 0 on clean tree | command / `make check` | exit 0 | Wave-Execution-INIT-REALWORLD-001-W0.md § TASK-W0-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `make check` | python-tooling incremental | ADR-001 | feature/INIT-REALWORLD-001-w0-seat-bulletin |
| TASK-W0-02 | Register stops minting seat JWT; login remains sole seat issuer; duplicate identity fail-closed | REQ-08, REQ-09, REQ-10, REQ-11 | TASK-W0-01 | `app/api/routes/authentication.py` modify; `tests/test_api/test_routes/test_registration.py` modify; `tests/test_api/test_routes/test_login.py` modify | Register response has no usable seat token; login returns token; duplicate register fails closed; bad login fails closed | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; assertions green | Wave-Execution-INIT-REALWORLD-001-W0.md § TASK-W0-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | TDD FF-05 | feature/INIT-REALWORLD-001-w0-seat-bulletin |
| TASK-W0-03 | Keep guest bulletin reads ungated; ORDER BY `updated_at DESC, created_at DESC`; document client JWT discard as unseat (no logout RPC) | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-12, REQ-13, REQ-14, REQ-34 | TASK-W0-02 | `app/db/repositories/articles.py` modify; `app/api/routes/articles/articles_resource.py` modify; `tests/test_api/test_routes/test_articles.py` modify; `tests/test_api/test_routes/test_profiles.py` modify | Guest list/get/tag/profile succeed without Authorization; feed order newest-first on seeded ≥2 articles; protected mutate without bearer returns 401 | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; order + 401 assertions | Wave-Execution-INIT-REALWORLD-001-W0.md § TASK-W0-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | ADR-004; TDD FF-10 | feature/INIT-REALWORLD-001-w0-seat-bulletin |
| TASK-W0-04 | Co-ship CAP-01/CAP-02 live verify + fixtures; exclude OOS comments/feed/follow from covers | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-34 | TASK-W0-03 | `tests/verify/__init__.py` create; `tests/verify/verify_wave0_seat_bulletin.py` create; `tests/fixtures/cap-01-bulletin/stimulus.json` create; `tests/fixtures/cap-01-bulletin/expected.json` create; `tests/fixtures/cap-01-bulletin/cleanup.md` create; `tests/fixtures/cap-02-seat/stimulus.json` create; `tests/fixtures/cap-02-seat/expected.json` create; `tests/fixtures/cap-02-seat/cleanup.md` create; `tests/fixtures/j-01-guest-feed/stimulus.json` create; `tests/fixtures/j-05-register-login/stimulus.json` create | Script declares `prayog:covers:` including CAP-01, CAP-02, J-01, J-05; exits 0 against local compose | command / `poetry run python -m tests.verify.verify_wave0_seat_bulletin` | exit 0; PASS markers | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` | testing-verify-flows | ADR-001/004 | feature/INIT-REALWORLD-001-w0-seat-bulletin |

#### Files (W0)

| ID | Path | Action |
|----|------|--------|
| FILE-W0-01 | `Makefile` | modify |
| FILE-W0-02 | `tests/README.md` | create |
| FILE-W0-03 | `app/api/routes/authentication.py` | modify |
| FILE-W0-04 | `app/db/repositories/articles.py` | modify |
| FILE-W0-05 | `app/api/routes/articles/articles_resource.py` | modify |
| FILE-W0-06 | `tests/test_api/test_routes/test_registration.py` | modify |
| FILE-W0-07 | `tests/test_api/test_routes/test_login.py` | modify |
| FILE-W0-08 | `tests/test_api/test_routes/test_articles.py` | modify |
| FILE-W0-09 | `tests/test_api/test_routes/test_profiles.py` | modify |
| FILE-W0-10 | `tests/verify/__init__.py` | create |
| FILE-W0-11 | `tests/verify/verify_wave0_seat_bulletin.py` | create |
| FILE-W0-12 | `tests/fixtures/cap-01-bulletin/stimulus.json` | create |
| FILE-W0-13 | `tests/fixtures/cap-01-bulletin/expected.json` | create |
| FILE-W0-14 | `tests/fixtures/cap-01-bulletin/cleanup.md` | create |
| FILE-W0-15 | `tests/fixtures/cap-02-seat/stimulus.json` | create |
| FILE-W0-16 | `tests/fixtures/cap-02-seat/expected.json` | create |
| FILE-W0-17 | `tests/fixtures/cap-02-seat/cleanup.md` | create |
| FILE-W0-18 | `tests/fixtures/j-01-guest-feed/stimulus.json` | create |
| FILE-W0-19 | `tests/fixtures/j-05-register-login/stimulus.json` | create |

#### Tests (W0)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W0-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-08..14, REQ-34 / TASK-W0-02..03 |
| TEST-W0-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres via existing async fixtures — boundary: asyncpg) | REQ-01..07, REQ-34 |
| TEST-W0-L | live (smoke) | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` | CAP-01, CAP-02 / J-01, J-05, J-07, J-08, J-11, J-17 |

#### Verification Coverage (W0)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-01..07 guest bulletin | CAP-01 / J-01,J-02,J-03,J-04,J-17 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-08..14 seat lifecycle | CAP-02 / J-05,J-07,J-08,J-11 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | ADR-004 client discard |
| REQ-34 newest-first | CAP-01 / J-01 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |

#### Live-verification intent (W0)

| Field | Value |
|-------|-------|
| Applicable | yes — new product surface + new `tests/verify` |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-01, CAP-02 / J-01, J-05, J-07, J-08, J-11, J-17 |
| Fixture packs | `tests/fixtures/cap-01-bulletin/`, `tests/fixtures/cap-02-seat/`, `tests/fixtures/j-01-guest-feed/`, `tests/fixtures/j-05-register-login/` |
| Runtime head binding | Bound at `wave-acceptance` against the wave PR head under test (not filled at planning) |
| Prerequisites / dependencies | Postgres up; API reachable via realworld-local compose |
| Safe test data | Synthetic users/articles only — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave0_seat_bulletin` |
| Expected observations | Script exit 0; guest feed/open PASS; register-without-seat + login-seat PASS; unseat-by-dropping-bearer denies mutate |
| Human look-ats | API JSON responses for feed order + 401 after bearer omit → newest-first slugs; 401 on publish |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic users/articles per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

### Phase W1 — Seated publish + own-work revise/tags

**GOAL-W1:** Enforce ≥1 non-blank tag on create/update; add `tagList` update path; ownership edit/delete; immediate visibility; no server draft; co-ship CAP-03/CAP-04 live prove.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W1-01 | Require ≥1 non-blank tag on create; reject blank-only | REQ-15, REQ-16, REQ-17, REQ-18, REQ-19 | — | `app/models/schemas/articles.py` modify; `app/api/routes/articles/articles_resource.py` modify; `tests/test_api/test_routes/test_articles.py` modify | Zero-tag create returns 4xx and creates no article; tagged create appears in guest feed | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; create assertions | Wave-Execution-INIT-REALWORLD-001-W1.md § TASK-W1-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | pydantic-schemas | TDD FF-07 | feature/INIT-REALWORLD-001-w1-publish-revise |
| TASK-W1-02 | Add `tagList` to update schema/repo; refuse empty tag-set; keep ownership deny | REQ-20, REQ-21, REQ-22, REQ-23, REQ-24 | TASK-W1-01 | `app/models/schemas/articles.py` modify; `app/db/repositories/articles.py` modify; `app/api/routes/articles/articles_resource.py` modify; `tests/test_api/test_routes/test_articles.py` modify | Tag-set update moves lane membership; empty tag-set refused without mutating prior; peer edit/delete denied | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; lane + ownership assertions | Wave-Execution-INIT-REALWORLD-001-W1.md § TASK-W1-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | repository-pattern | TDD FF-06 | feature/INIT-REALWORLD-001-w1-publish-revise |
| TASK-W1-03 | Co-ship CAP-03/CAP-04 live verify + fixtures | REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21, REQ-22, REQ-23, REQ-24 | TASK-W1-02 | `tests/verify/verify_wave1_publish_revise.py` create; `tests/fixtures/cap-03-publish/stimulus.json` create; `tests/fixtures/cap-03-publish/expected.json` create; `tests/fixtures/cap-03-publish/cleanup.md` create; `tests/fixtures/cap-04-revise/stimulus.json` create; `tests/fixtures/cap-04-revise/expected.json` create; `tests/fixtures/cap-04-revise/cleanup.md` create; `tests/fixtures/j-06-publish/stimulus.json` create; `tests/fixtures/j-09-own-revise/stimulus.json` create; `tests/fixtures/j-15-retag/stimulus.json` create | Script `prayog:covers:` includes CAP-03, CAP-04, J-06, J-09; exits 0 on compose | command / `poetry run python -m tests.verify.verify_wave1_publish_revise` | exit 0; PASS markers | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run python -m tests.verify.verify_wave1_publish_revise` | testing-verify-flows | ADR-001 | feature/INIT-REALWORLD-001-w1-publish-revise |

#### Files (W1)

| ID | Path | Action |
|----|------|--------|
| FILE-W1-01 | `app/models/schemas/articles.py` | modify |
| FILE-W1-02 | `app/db/repositories/articles.py` | modify |
| FILE-W1-03 | `app/api/routes/articles/articles_resource.py` | modify |
| FILE-W1-04 | `tests/test_api/test_routes/test_articles.py` | modify |
| FILE-W1-05 | `tests/verify/verify_wave1_publish_revise.py` | create |
| FILE-W1-06 | `tests/fixtures/cap-03-publish/stimulus.json` | create |
| FILE-W1-07 | `tests/fixtures/cap-03-publish/expected.json` | create |
| FILE-W1-08 | `tests/fixtures/cap-03-publish/cleanup.md` | create |
| FILE-W1-09 | `tests/fixtures/cap-04-revise/stimulus.json` | create |
| FILE-W1-10 | `tests/fixtures/cap-04-revise/expected.json` | create |
| FILE-W1-11 | `tests/fixtures/cap-04-revise/cleanup.md` | create |
| FILE-W1-12 | `tests/fixtures/j-06-publish/stimulus.json` | create |
| FILE-W1-13 | `tests/fixtures/j-09-own-revise/stimulus.json` | create |
| FILE-W1-14 | `tests/fixtures/j-15-retag/stimulus.json` | create |

#### Tests (W1)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W1-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-15..24 / TASK-W1-01..02 |
| TEST-W1-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres tag links boundary) | REQ-21 |
| TEST-W1-L | live (smoke) | `poetry run python -m tests.verify.verify_wave1_publish_revise` | CAP-03, CAP-04 / J-06, J-09, J-10, J-12, J-15, J-18 |

#### Verification Coverage (W1)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-15..19 publish | CAP-03 / J-06,J-08,J-12,J-18 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-20..24 revise/ownership | CAP-04 / J-09,J-10,J-15 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |

#### Live-verification intent (W1)

| Field | Value |
|-------|-------|
| Applicable | yes |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-03, CAP-04 / J-06, J-09, J-10, J-12, J-15, J-18 |
| Fixture packs | `tests/fixtures/cap-03-publish/`, `tests/fixtures/cap-04-revise/`, `tests/fixtures/j-06-publish/`, `tests/fixtures/j-09-own-revise/`, `tests/fixtures/j-15-retag/` |
| Runtime head binding | Bound at `wave-acceptance` |
| Prerequisites / dependencies | W0 seat+bulletin green; Postgres + API up |
| Safe test data | Synthetic authors/articles/tags |
| Steps / command | `poetry run python -m tests.verify.verify_wave1_publish_revise` |
| Expected observations | Tagged publish visible to guest; zero-tag refused; retag moves lanes; peer mutate denied |
| Human look-ats | Guest feed contains new slug; peer PUT/DELETE → 403; empty-tag update unchanged |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop |

---

### Phase W2 — Private shelf + nameplate + as-built

**GOAL-W2:** Owner-scoped shelf listing (ADR-002), `favoritesCount=0` (ADR-003), own-favorite / missing-favorite fail-closed, nameplate identity lock; co-ship CAP-05/CAP-06 live prove; seed as-built detail + index row.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W2-01 | Gate `favorited=` to seated owner; force `favoritesCount=0`; refuse own favorite; missing/deleted favorite 404; invert unit polarity | REQ-25, REQ-26, REQ-27, REQ-28, REQ-29, REQ-33, REQ-35 | — | `app/api/routes/articles/articles_resource.py` modify; `app/api/routes/articles/articles_common.py` modify; `app/db/repositories/articles.py` modify; `tests/test_api/test_routes/test_articles.py` modify | Peer/guest `favorited=` denied (403); owner shelf lists own favorites; favoritesCount always 0; own-favorite refused; missing favorite 404; deleted article not resurrected via shelf | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; polarity inverted vs prior Conduit test | Wave-Execution-INIT-REALWORLD-001-W2.md § TASK-W2-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | ADR-002, ADR-003 | feature/INIT-REALWORLD-001-w2-shelf-nameplate |
| TASK-W2-02 | Lock username/email on self-update; bio/image apply; peer has no update route | REQ-30, REQ-31, REQ-32 | TASK-W2-01 | `app/models/schemas/users.py` modify; `app/api/routes/users.py` modify; `tests/test_api/test_routes/test_users.py` modify | Identity fields rejected/ignored; bio/image reflected on public profile; unseated update 401 | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; identity lock assertions | Wave-Execution-INIT-REALWORLD-001-W2.md § TASK-W2-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | pydantic-schemas | TDD FF-09 | feature/INIT-REALWORLD-001-w2-shelf-nameplate |
| TASK-W2-03 | Co-ship CAP-05/CAP-06 live verify + fixtures; seed as-built detail + index | REQ-25, REQ-26, REQ-27, REQ-28, REQ-29, REQ-30, REQ-31, REQ-32, REQ-33, REQ-35 | TASK-W2-02 | `tests/verify/verify_wave2_shelf_nameplate.py` create; `tests/fixtures/cap-05-shelf/stimulus.json` create; `tests/fixtures/cap-05-shelf/expected.json` create; `tests/fixtures/cap-05-shelf/cleanup.md` create; `tests/fixtures/cap-06-nameplate/stimulus.json` create; `tests/fixtures/cap-06-nameplate/expected.json` create; `tests/fixtures/cap-06-nameplate/cleanup.md` create; `tests/fixtures/j-13-shelf-nameplate/stimulus.json` create; `tests/fixtures/j-16-shelf-privacy/stimulus.json` create; `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-001.md` create; `docs/specification/as-built/implementation-status.md` create | Live script covers CAP-05, CAP-06, J-13, J-16; exits 0; as-built detail + index pointer exist | command / `poetry run python -m tests.verify.verify_wave2_shelf_nameplate` | exit 0; as-built files present | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-001-api.md` | `poetry run python -m tests.verify.verify_wave2_shelf_nameplate` | testing-verify-flows; SDD as-built | ADR-002, ADR-003 | feature/INIT-REALWORLD-001-w2-shelf-nameplate |

#### Files (W2)

| ID | Path | Action |
|----|------|--------|
| FILE-W2-01 | `app/api/routes/articles/articles_resource.py` | modify |
| FILE-W2-02 | `app/api/routes/articles/articles_common.py` | modify |
| FILE-W2-03 | `app/db/repositories/articles.py` | modify |
| FILE-W2-04 | `app/models/schemas/users.py` | modify |
| FILE-W2-05 | `app/api/routes/users.py` | modify |
| FILE-W2-06 | `tests/test_api/test_routes/test_articles.py` | modify |
| FILE-W2-07 | `tests/test_api/test_routes/test_users.py` | modify |
| FILE-W2-08 | `tests/verify/verify_wave2_shelf_nameplate.py` | create |
| FILE-W2-09 | `tests/fixtures/cap-05-shelf/stimulus.json` | create |
| FILE-W2-10 | `tests/fixtures/cap-05-shelf/expected.json` | create |
| FILE-W2-11 | `tests/fixtures/cap-05-shelf/cleanup.md` | create |
| FILE-W2-12 | `tests/fixtures/cap-06-nameplate/stimulus.json` | create |
| FILE-W2-13 | `tests/fixtures/cap-06-nameplate/expected.json` | create |
| FILE-W2-14 | `tests/fixtures/cap-06-nameplate/cleanup.md` | create |
| FILE-W2-15 | `tests/fixtures/j-13-shelf-nameplate/stimulus.json` | create |
| FILE-W2-16 | `tests/fixtures/j-16-shelf-privacy/stimulus.json` | create |
| FILE-W2-17 | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-001.md` | create |
| FILE-W2-18 | `docs/specification/as-built/implementation-status.md` | create |

#### Tests (W2)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W2-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-25..33, REQ-35 / TASK-W2-01..02 |
| TEST-W2-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (favorites join boundary) | REQ-27 |
| TEST-W2-L | live (smoke) | `poetry run python -m tests.verify.verify_wave2_shelf_nameplate` | CAP-05, CAP-06 / J-13, J-16, J-19 |

#### Verification Coverage (W2)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-25..29,33,35 shelf | CAP-05 / J-13,J-16 | TEST-W2-U | TEST-W2-I | TEST-W2-L | N/A | ADR-002/003 |
| REQ-30..32 nameplate | CAP-06 / J-13,J-19 | TEST-W2-U | N/A | TEST-W2-L | N/A | |

#### Live-verification intent (W2)

| Field | Value |
|-------|-------|
| Applicable | yes |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-05, CAP-06 / J-13, J-16, J-19 |
| Fixture packs | `tests/fixtures/cap-05-shelf/`, `tests/fixtures/cap-06-nameplate/`, `tests/fixtures/j-13-shelf-nameplate/`, `tests/fixtures/j-16-shelf-privacy/` |
| Runtime head binding | Bound at `wave-acceptance` |
| Prerequisites / dependencies | W0+W1 green; multi-user synthetic actors |
| Safe test data | Synthetic members A/B; articles by A favorited by B |
| Steps / command | `poetry run python -m tests.verify.verify_wave2_shelf_nameplate` |
| Expected observations | B cannot list A shelf; favoritesCount=0; own-favorite refused; nameplate bio/image updates; identity fields unchanged |
| Human look-ats | Peer `favorited=A` → 403; public profile shows bio/image only change |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop |

---

## 3. Dependencies (DEP)

| ID | Dependency | Blocks |
|----|------------|--------|
| DEP-01 | Accepted ADR-001..004 + refreshed Lint evidence | Plan AUTHORIZE (satisfied this pass) |
| DEP-02 | W0 seat+bulletin before W1 publish prove | W1 live acceptance |
| DEP-03 | W1 publish before W2 shelf/delete interactions | W2 live acceptance |
| DEP-04 | realworld-local compose for live smoke | Human wave-acceptance |
| DEP-05 | Q-05 / Q-09 remain deferred with defaults | Multi-session revoke; mid-read push |

---

## 4. Risks (RISK)

| ID | Risk | Mitigation |
|----|------|------------|
| RISK-01 | Retaining `app/` conflicts with platform `src/` MDC | Accepted ADR-001 Wave0a exception; document in TASK MDC notes |
| RISK-02 | Baseline privacy/seat drifts remain until waves land | FF-05..10 mapped to concrete TASKs |
| RISK-03 | OOS Conduit routes (comments/feed/follow) confuse prove | Exclude from `prayog:covers` (AF-4) |
| RISK-04 | `make check` weaker than full pyright/import-linter | Explicit ADR-001 incremental tooling; later INIT may tighten |
| RISK-05 | Client JWT discard leaves stolen-token window | Accepted ADR-004; Q-05 deferred |
| RISK-06 | Live prove depends on realworld-local | DEP-04; stop conditions on compose failure |
| RISK-07 | Coverage 100% gate in pytest may fight inverted tests | Keep suite green while changing polarity; no coverage lowering without PE note |

---

## 5. Out of scope

- realworld-web UAT chrome / kill-path driving
- realworld-local compose product ownership (env only)
- Comments, follows, personalized feeds, OAuth, public who-favorited proof
- Drafts/moderation, password recovery, account deletion, admin roles
- Multi-session token cascade (Q-05 / IM-05 deferred)
- Mid-read push after delete (Q-09 / IM-09 deferred)
- Platform `src/` chassis migration (beyond ADR-001 Wave0a exception)
- Board seeding / GitHub issues (post-merge `/create-board-tickets` only)
- Product code implementation in this skill pass

---

## 6. As-built and docs tasks

> Update these in the **same PR** as the code they describe.

| Task | File | Action |
|------|------|--------|
| Create/update per-initiative as-built detail | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-001.md` | create in W2 (TASK-W2-03) |
| Update as-built index row | `docs/specification/as-built/implementation-status.md` | create/overwrite pointer row in W2 |
| Ensure live-verify coverage marker | co-shipped `tests/verify/verify_wave*.py` | Self-declare `prayog:covers:` — do **not** use `tests/README.md` as SSOT |

> **ADR lifecycle** — Accepted during `technical-review-approval`. Planning consumes Accepted files only.

---

## 7. Plan check summary

| Check | Status | Notes |
|-------|--------|-------|
| P1 | PASS | All REQ-01..35 in §1; each wave Implements cites product REQs |
| P2 | PASS | Every REQ has ≥1 TASK; every TASK Implements ≥1 REQ-* |
| P3 | PASS | Every TASK lists FILE paths |
| P4 | PASS | Observable exit + proof + expected + evidence_expected on each TASK |
| P5 | PASS | Verification Coverage maps REQs to unit/integration/smoke; live not unit |
| P6 | PASS | No product scope beyond initiative spec |
| P7 | PASS | FF-01..04 → Accepted ADRs; FF-05..10 → TASKs; Q-05/Q-09 deferred with owner+default |
| P8 | PASS | W0→W1→W2 depends_on documented |
| P9 | PASS | As-built detail + index in W2 same-PR as shelf/nameplate |
| P10 | PASS | Self-contained; commands RESOLVED; live env prerequisites stated |
| P11 | PASS | MDC notes on TASKs; ADR-001 exception for chassis |
| P12 | PASS | All ADR_REQUIRED files Accepted and linked in §0 |
| P13 | PASS | PE sign-off complete; boundary fields false; plan-time lint verify PASS on 4 ADRs |
| P14 | PASS | §9 WorkManifest with W0..W2, tasks[], verification, body tables |
| P15 | PASS | Each coding wave co-ships live verify + fixtures; overlap check recorded (dir absent → new FILEs); covers include CAP/J |
| P16 | PASS | `workmanifest_contract.py` exit 0 on §9 (recorded after write) |

### P13 lint invocation (executed 2026-11-11)

```text
python3 prayog-skills/scripts/adr_boundary_lint.py docs/specification/adr/adr-00N-….md \
  --strict --verify-lint-evidence \
  --source-text /tmp/init-rw001-t12/all-approved-reqs.txt \
  --source-text /tmp/init-rw001-t12/FF-0N-evidence.txt \
  --finding-text-file /tmp/init-rw001-t12/FF-0N-finding.txt \
  --approved-req-id REQ-01 … REQ-35
```

| ADR | Lint evidence digest | Result |
|-----|----------------------|--------|
| ADR-001 | `7ca16d679b23b1f2081b62ea858da9ee4fe7977573bd3ab24bea05a3ae89ebbd` | PASS |
| ADR-002 | `50e68d173f70b855d87cc1bec0893ca7ae95627f82d24aa06452434c495bf7dd` | PASS |
| ADR-003 | `8c47027141d5c9a816acc015aaeb270f0900e8923b774c1567c2fb1d39f8bf31` | PASS |
| ADR-004 | `6e22d2b04315470df42880cf4efeb8c50e73b74f231bbec7e418126d21e75f41` | PASS |

---

## 8. Forge / PR instructions

> Persist this plan locally and publish via `/commit-workspace` to the
> **Draft spec PR** branch alongside spec, feasibility, TDD, and Accepted ADRs.
> Do **not** commit inside this skill. Label remains **`spec-pending`** until PE
> completes §10.

```
Branch:   docs/spec-init-realworld-001  (Draft PR)
PR title: "[INIT-REALWORLD-001] Spec — realworld-api"
PR:       https://github.com/drivestream-lab/realworld-api/pull/3
PR body:  link meta PRD PR; paste §1 Requirements table + wave goals summary

Required reviewers: @drivestream-lab/backend-devs
Review deadline: 2026-11-16

PE checklist (before spec-lgtm):
  [ ] Spec + feasibility + TDD + Accepted ADRs + this plan on current head
  [ ] §0 PE sign-off on TDD marked complete
  [ ] Wave order and dependencies make sense
  [ ] Done-when / exit criteria are observable and testable (P4)
  [ ] Verification Coverage maps every criterion to a layer (P5)
  [ ] WorkManifest YAML (§9) passes workmanifest-contract-pass (P16) — prayog/v1
  [ ] P1–P16 checks all pass (including P15 co-ship)

After spec-lgtm + Approve + merge — **/create-board-tickets** from §9 (post-merge only)
```

---

## 10. Coding-readiness unlock (PE — after plan on head)

| Item | Value |
|------|-------|
| Workflow outcome | `pass` — P1–P16 PASS; Accepted TDD/ADRs; plan ready for coding-readiness |
| Verdict | GATE OPEN REQUEST |
| Spec PR | https://github.com/drivestream-lab/realworld-api/pull/3 |
| Spec PR head SHA | `266c56b405646c28b1ffc1144e1a9e7800304c2b` (remote tip at plan time; refresh after Forge publish) |
| Gate label (current) | `spec-pending` |
| Gate label (target) | `spec-lgtm` |
| Local plan path | `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md` |
| Forge readiness | fill `handoff.forge` for `/commit-workspace` — do not commit inside this skill |
| Blocking items | none |
| plan_digest | sha256:6718e52292d08a90f7959efa887f39cd9f4f226b74dc657b52c5f2ed4f619d27 |

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
initiative: INIT-REALWORLD-001
spec_pr_head_sha: {SHA after plan Forge publish}
meta_pr_head_sha: a500df8eeefbea095ecdd65e00edb128416c3cf4
impact_map_revision: 1
prd_digest: sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4
scope_digest: sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d
plan_digest: sha256:6718e52292d08a90f7959efa887f39cd9f4f226b74dc657b52c5f2ed4f619d27
artifacts:
  - docs/specification/product/INIT-REALWORLD-001-api.md
  - docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-001.md
  - docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md
  - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md
  - docs/specification/adr/adr-001-wave0a-package-chassis.md
  - docs/specification/adr/adr-002-private-shelf-list-authorization.md
  - docs/specification/adr/adr-003-favorites-count-wire-policy.md
  - docs/specification/adr/adr-004-wave0a-unseat-token-discard.md
```

| PE action | Remove | Add |
|-----------|--------|-----|
| Pending/new revision | `spec-lgtm`, `spec-blocked` | `spec-pending` |
| Request changes/hold | `spec-pending`, `spec-lgtm` | `spec-blocked` |
| Approve full package | `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale` | `spec-lgtm` |

---

## 9. WorkManifest seed

> Primary: `/create-board-tickets` creates one GitHub Issue per wave after spec merge.
> Validate: `PYTHONPATH=prayog-skills:. python3 prayog-skills/scripts/workmanifest_contract.py` on this plan (P16).
> `target.org` / `target.project` from `realworld-meta/config/governance-drivestream-lab.yaml` (`project_board.name: RealWorld`).

```yaml
# Generated by /spec-implementation-plan — 2026-11-11
# LOCAL — do not commit to prayog-skills upstream
apiVersion: prayog/v1
kind: WorkManifest

initiative: INIT-REALWORLD-001

metadata:
  title: INIT-REALWORLD-001 — Public bulletin with session-bound contribution seat
  summary: |
    Provider for CAP-01..CAP-06 / CTR-01..CTR-06 on legacy Conduit app/ chassis
    (ADR-001): seat lifecycle, ungated bulletin, tagged publish/revise, private
    shelf isolation, and own nameplate — with co-shipped live verify per wave.
  playbook:
    - docs/specification/product/INIT-REALWORLD-001-api.md
    - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md

target:
  org: drivestream-lab
  project: RealWorld

defaults:
  initiative: INIT-REALWORLD-001
  parent: EPIC
  labels:
    - INIT-REALWORLD-001

epic:
  id: EPIC
  repo: realworld-api
  title: "[feature] INIT-REALWORLD-001 — Wave0a API provider (bulletin + seat)"
  codebase: realworld-api
  spec_path: docs/specification/product/INIT-REALWORLD-001-api.md
  verify_command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
  body: |
    ## Objective

    Deliver the realworld-api provider for Wave0a UAT kill paths: guest bulletin
    read, seated tagged publish, and post-logout contribution denial — plus
    private shelf and nameplate surfaces required by CAP-01..CAP-06.

    ## Waves

    | Wave | Goal |
    |------|------|
    | W0 | Seat + public bulletin + feed order + prove scaffold |
    | W1 | Seated publish + own-work revise/tags |
    | W2 | Private shelf + nameplate + as-built |

    ## References

    - Spec: docs/specification/product/INIT-REALWORLD-001-api.md
    - Implementation plan: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md
    - Technical review: docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md

work:
  - id: W0
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-001 W0] Seat + public bulletin + feed order + prove scaffold"
    depends_on: []
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-001-api.md
    verify_command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
    tasks:
      - id: TASK-W0-01
        implements: [REQ-01]
        depends_on: []
        files:
          - path: Makefile
            action: modify
          - path: tests/README.md
            action: create
        exit:
          criteria:
            - "make check exits 0 on a clean tree after Makefile check target exists"
          proof:
            kind: command
            command: make check
            expected: "exit 0"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W0.md § TASK-W0-01"
      - id: TASK-W0-02
        implements: [REQ-08, REQ-09, REQ-10, REQ-11]
        depends_on: [TASK-W0-01]
        files:
          - path: app/api/routes/authentication.py
            action: modify
          - path: tests/test_api/test_routes/test_registration.py
            action: modify
          - path: tests/test_api/test_routes/test_login.py
            action: modify
        exit:
          criteria:
            - "Register response has no usable seat token; login returns token; duplicate register and bad login fail closed"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; seat assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W0.md § TASK-W0-02"
      - id: TASK-W0-03
        implements: [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-12, REQ-13, REQ-14, REQ-34]
        depends_on: [TASK-W0-02]
        files:
          - path: app/db/repositories/articles.py
            action: modify
          - path: app/api/routes/articles/articles_resource.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
          - path: tests/test_api/test_routes/test_profiles.py
            action: modify
        exit:
          criteria:
            - "Guest bulletin reads succeed without Authorization; feed order newest-first; mutate without bearer returns 401"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; order and 401 assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W0.md § TASK-W0-03"
      - id: TASK-W0-04
        implements: [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-34]
        depends_on: [TASK-W0-03]
        files:
          - path: tests/verify/__init__.py
            action: create
          - path: tests/verify/verify_wave0_seat_bulletin.py
            action: create
          - path: tests/fixtures/cap-01-bulletin/stimulus.json
            action: create
          - path: tests/fixtures/cap-01-bulletin/expected.json
            action: create
          - path: tests/fixtures/cap-01-bulletin/cleanup.md
            action: create
          - path: tests/fixtures/cap-02-seat/stimulus.json
            action: create
          - path: tests/fixtures/cap-02-seat/expected.json
            action: create
          - path: tests/fixtures/cap-02-seat/cleanup.md
            action: create
          - path: tests/fixtures/j-01-guest-feed/stimulus.json
            action: create
          - path: tests/fixtures/j-05-register-login/stimulus.json
            action: create
        exit:
          criteria:
            - "Live verify module exits 0 against local compose with prayog:covers including CAP-01 and CAP-02"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
            expected: "exit 0; PASS markers for CAP-01/CAP-02"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave0_seat_bulletin
        covers: [CAP-01, CAP-02, J-01, J-05, J-07, J-08, J-11, J-17, REQ-01, REQ-08, REQ-10, REQ-12, REQ-34]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-01-bulletin/stimulus.json
          - tests/fixtures/cap-02-seat/stimulus.json
          - tests/fixtures/j-01-guest-feed/stimulus.json
          - tests/fixtures/j-05-register-login/stimulus.json
        prerequisites:
          - "realworld-local compose up with API reachable"
        safe_test_data:
          - "synthetic users and articles only"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave0_seat_bulletin"
        expected_observations:
          - "Script exit 0; guest feed/open PASS; register without seat + login seat PASS; bearer omit denies mutate"
        human_observations:
          - locus: "API JSON feed order + 401 after bearer omit"
            expect: "newest-first slugs; 401 on publish"
            covers: [CAP-01, CAP-02]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic users/articles per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Seat + public bulletin + feed order + prove scaffold

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W0-01 | REQ-01 | — | make check exits 0 | command/make check |
      | TASK-W0-02 | REQ-08, REQ-09, REQ-10, REQ-11 | TASK-W0-01 | register/login seat rules | command/pytest |
      | TASK-W0-03 | REQ-01..07, REQ-12..14, REQ-34 | TASK-W0-02 | guest reads + order + 401 | command/pytest |
      | TASK-W0-04 | REQ-01..14, REQ-34 | TASK-W0-03 | live CAP-01/CAP-02 | command/verify_wave0 |

      ## Done when

      - [ ] All W0 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-001-api.md

  - id: W1
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-001 W1] Seated publish + own-work revise/tags"
    depends_on:
      - W0
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-001-api.md
    verify_command: poetry run python -m tests.verify.verify_wave1_publish_revise
    tasks:
      - id: TASK-W1-01
        implements: [REQ-15, REQ-16, REQ-17, REQ-18, REQ-19]
        depends_on: []
        files:
          - path: app/models/schemas/articles.py
            action: modify
          - path: app/api/routes/articles/articles_resource.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
        exit:
          criteria:
            - "Zero-tag create returns 4xx with no article; tagged create appears in guest feed"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; create assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W1.md § TASK-W1-01"
      - id: TASK-W1-02
        implements: [REQ-20, REQ-21, REQ-22, REQ-23, REQ-24]
        depends_on: [TASK-W1-01]
        files:
          - path: app/models/schemas/articles.py
            action: modify
          - path: app/db/repositories/articles.py
            action: modify
          - path: app/api/routes/articles/articles_resource.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
        exit:
          criteria:
            - "Tag-set update moves lanes; empty tag-set refused; peer edit/delete denied"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; lane and ownership assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W1.md § TASK-W1-02"
      - id: TASK-W1-03
        implements: [REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21, REQ-22, REQ-23, REQ-24]
        depends_on: [TASK-W1-02]
        files:
          - path: tests/verify/verify_wave1_publish_revise.py
            action: create
          - path: tests/fixtures/cap-03-publish/stimulus.json
            action: create
          - path: tests/fixtures/cap-03-publish/expected.json
            action: create
          - path: tests/fixtures/cap-03-publish/cleanup.md
            action: create
          - path: tests/fixtures/cap-04-revise/stimulus.json
            action: create
          - path: tests/fixtures/cap-04-revise/expected.json
            action: create
          - path: tests/fixtures/cap-04-revise/cleanup.md
            action: create
          - path: tests/fixtures/j-06-publish/stimulus.json
            action: create
          - path: tests/fixtures/j-09-own-revise/stimulus.json
            action: create
          - path: tests/fixtures/j-15-retag/stimulus.json
            action: create
        exit:
          criteria:
            - "Live verify exits 0 with prayog:covers including CAP-03 and CAP-04"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave1_publish_revise
            expected: "exit 0; PASS markers for CAP-03/CAP-04"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave1_publish_revise
        covers: [CAP-03, CAP-04, J-06, J-09, J-10, J-12, J-15, J-18, REQ-15, REQ-20, REQ-24]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-03-publish/stimulus.json
          - tests/fixtures/cap-04-revise/stimulus.json
          - tests/fixtures/j-06-publish/stimulus.json
          - tests/fixtures/j-09-own-revise/stimulus.json
          - tests/fixtures/j-15-retag/stimulus.json
        prerequisites:
          - "W0 seat+bulletin green; compose up"
        safe_test_data:
          - "synthetic authors/articles/tags"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave1_publish_revise"
        expected_observations:
          - "Tagged publish visible to guest; zero-tag refused; retag moves lanes; peer mutate denied"
        human_observations:
          - locus: "Guest feed + peer PUT/DELETE responses"
            expect: "new slug present; peer mutate 403; empty-tag update unchanged"
            covers: [CAP-03, CAP-04]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic articles/tags per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Seated publish + own-work revise/tags

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W1-01 | REQ-15..19 | — | tag create rules | command/pytest |
      | TASK-W1-02 | REQ-20..24 | TASK-W1-01 | tag update + ownership | command/pytest |
      | TASK-W1-03 | REQ-15..24 | TASK-W1-02 | live CAP-03/CAP-04 | command/verify_wave1 |

      ## Done when

      - [ ] All W1 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-001-api.md

  - id: W2
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-001 W2] Private shelf + nameplate + as-built"
    depends_on:
      - W1
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-001-api.md
    verify_command: poetry run python -m tests.verify.verify_wave2_shelf_nameplate
    tasks:
      - id: TASK-W2-01
        implements: [REQ-25, REQ-26, REQ-27, REQ-28, REQ-29, REQ-33, REQ-35]
        depends_on: []
        files:
          - path: app/api/routes/articles/articles_resource.py
            action: modify
          - path: app/api/routes/articles/articles_common.py
            action: modify
          - path: app/db/repositories/articles.py
            action: modify
          - path: tests/test_api/test_routes/test_articles.py
            action: modify
        exit:
          criteria:
            - "Peer/guest favorited filter denied; owner shelf works; favoritesCount always 0; own/missing favorite fail closed; no resurrection after delete"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; shelf polarity and count assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W2.md § TASK-W2-01"
      - id: TASK-W2-02
        implements: [REQ-30, REQ-31, REQ-32]
        depends_on: [TASK-W2-01]
        files:
          - path: app/models/schemas/users.py
            action: modify
          - path: app/api/routes/users.py
            action: modify
          - path: tests/test_api/test_routes/test_users.py
            action: modify
        exit:
          criteria:
            - "username/email locked on self-update; bio/image apply; unseated update 401"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; identity lock assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-001-W2.md § TASK-W2-02"
      - id: TASK-W2-03
        implements: [REQ-25, REQ-26, REQ-27, REQ-28, REQ-29, REQ-30, REQ-31, REQ-32, REQ-33, REQ-35]
        depends_on: [TASK-W2-02]
        files:
          - path: tests/verify/verify_wave2_shelf_nameplate.py
            action: create
          - path: tests/fixtures/cap-05-shelf/stimulus.json
            action: create
          - path: tests/fixtures/cap-05-shelf/expected.json
            action: create
          - path: tests/fixtures/cap-05-shelf/cleanup.md
            action: create
          - path: tests/fixtures/cap-06-nameplate/stimulus.json
            action: create
          - path: tests/fixtures/cap-06-nameplate/expected.json
            action: create
          - path: tests/fixtures/cap-06-nameplate/cleanup.md
            action: create
          - path: tests/fixtures/j-13-shelf-nameplate/stimulus.json
            action: create
          - path: tests/fixtures/j-16-shelf-privacy/stimulus.json
            action: create
          - path: docs/specification/as-built/Implementation-Status-INIT-REALWORLD-001.md
            action: create
          - path: docs/specification/as-built/implementation-status.md
            action: create
        exit:
          criteria:
            - "Live verify exits 0 with CAP-05/CAP-06 covers; as-built detail and index pointer files exist"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave2_shelf_nameplate
            expected: "exit 0; as-built files present"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave2_shelf_nameplate
        covers: [CAP-05, CAP-06, J-13, J-16, J-19, REQ-25, REQ-27, REQ-30, REQ-33, REQ-35]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-05-shelf/stimulus.json
          - tests/fixtures/cap-06-nameplate/stimulus.json
          - tests/fixtures/j-13-shelf-nameplate/stimulus.json
          - tests/fixtures/j-16-shelf-privacy/stimulus.json
        prerequisites:
          - "W0+W1 green; multi-user synthetic actors available"
        safe_test_data:
          - "synthetic members A/B; articles by A favorited by B"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave2_shelf_nameplate"
        expected_observations:
          - "B cannot list A shelf; favoritesCount=0; own-favorite refused; nameplate bio/image updates with identity fields unchanged"
        human_observations:
          - locus: "Peer favorited=A response + public profile fields"
            expect: "403 for peer shelf; bio/image changed only"
            covers: [CAP-05, CAP-06]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic users/favorites per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Private shelf + nameplate + as-built

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W2-01 | REQ-25..29,33,35 | — | shelf isolation + count | command/pytest |
      | TASK-W2-02 | REQ-30..32 | TASK-W2-01 | nameplate identity lock | command/pytest |
      | TASK-W2-03 | REQ-25..33,35 | TASK-W2-02 | live CAP-05/06 + as-built | command/verify_wave2 |

      ## Done when

      - [ ] All W2 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-001-api.md```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-implementation-plan
  outcome: pass
  artifact:
    path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md
    digest: sha256:6718e52292d08a90f7959efa887f39cd9f4f226b74dc657b52c5f2ed4f619d27
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4
    scope_digest: sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d
    meta_pr_approved_head: a500df8eeefbea095ecdd65e00edb128416c3cf4
    draft_spec_pr: https://github.com/drivestream-lab/realworld-api/pull/3
    workmanifest_contract: pass
    p15_overlap: tests/verify absent — new FILEs warranted
    codegraph_provider: degraded-none
    grounding_depth: deep
    plan_status: Planned
  next_candidates:
    - coding-readiness
  human_checkpoint: true
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-001] Spec — realworld-api (implementation plan)"
    body_path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-001.md
    target_branch: docs/spec-init-realworld-001
```
