---
goal: INIT-REALWORLD-004 — implementation plan
initiative: INIT-REALWORLD-004
status: Planned
date_created: 2026-11-12
source_spec: docs/specification/product/INIT-REALWORLD-004-api.md
feasibility_report: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md
technical_review: docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md
prd_digest: sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3
impact_map: realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-004.md
impact_map_revision: 1
repo_scope_digest: sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5
approved_meta_pr_head: 02c74d94cf8748c1cd53a268035a8a84433caf94
branch: chore/INIT-REALWORLD-004-spec-realworld-api
review_deadline: 2026-11-17
deciders: PE — spec-lgtm + Approve on exact head after full package
---

# Implementation plan — INIT-REALWORLD-004

## Source freshness and command contract

| Item | Value | Status |
|------|-------|--------|
| Spec | `docs/specification/product/INIT-REALWORLD-004-api.md` | CURRENT — live digest `sha256:a33f3891abdb9a5f25380469eb13313260b1a64e540b69453d77102a2116b459` matches TDD citation; H1 PRD digest matches meta PRD |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md` | CURRENT — same H1/H2/H3/G1; tip continuous into Accepted TDD (`new_adr: false`) |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md` | CURRENT — `Status: Accepted`; ADR_REQUIRED 0; Q-11 + E-01..E-07 resolved TDD_ONLY |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-004.md` / `1` | CURRENT |
| Repo scope digest | `sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5` | CURRENT — api row CAP-01..CAP-03 |
| Approved meta PR head | `02c74d94cf8748c1cd53a268035a8a84433caf94` | CURRENT — meta PR #12 |
| `check_command` | `make check` | RESOLVED — W0 co-ships Makefile `check` target (`poetry run black --check app tests`); ADR-001 allows incremental tooling vs full pyright/import-linter |
| `test_command` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | RESOLVED |
| `verify_command` | Wave-scoped live modules under `tests/verify/` (W0 `poetry run python -m tests.verify.verify_wave0_followed_tags_establish`; W1 `poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship`) | RESOLVED — co-shipped with product surface (P15); not unit |
| `ground_command` | N/A — as-built seeded in W1; `/ground-spec` after wave-acceptance (FF-02 / AF-2) | N/A — reason recorded |

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md` |
| Technical review status | Accepted |
| PE sign-off | [x] complete — 2026-11-12 (TDD `Status: Accepted`; zero ADR_REQUIRED; light-confirmation TDD under ADR-001/004; Hermes non-interactive lock) |
| Resolved ADRs | none required — light confirmation, zero NEW-ADR findings. Constraining baseline: [`adr-001-wave0a-package-chassis.md`](../adr/adr-001-wave0a-package-chassis.md) (Accepted — continue `app/`); [`adr-004-wave0a-unseat-token-discard.md`](../adr/adr-004-wave0a-unseat-token-discard.md) (Accepted — unseat = client JWT discard; tag-follow rows survive reseat). ADR-002/003 independent (favorites / favoritesCount). |
| ADR product-boundary re-check | Zero ADR_REQUIRED — no new ADR lint targets. Constraining ADR-001/ADR-004: `changes_user_visible_behavior: false` / `spec_amendment_required: false` confirmed by file read (2026-11-12). Structure lint `adr_boundary_lint.py --require-sources` with INIT-004 spec REQ rows + feasibility FF-03 evidence → PASS (`sources_checked=2`) for both ADRs and TDD `--tdd`. Prior-INIT `--verify-lint-evidence` digest recompute against reconstructed INIT-004 source pack mismatches original T12 source pack (unavailable) — recorded as Should-fix note, not a Draft/unaccepted gate. |
| Outstanding PM questions | none blocking — Q-07..Q-10 open later / Out of scope with Impact-Map defaults |
| Outstanding domain questions | none — all resolved |

> Do not start W0 implementation until PE sign-off is marked complete above.

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | package chassis / `app/` vs `src/` | Accepted — continue (Q-11) |
| ADR-002 | private-shelf `favorited=` authorization | Accepted — out of INIT-004 CAP scope |
| ADR-003 | `favoritesCount` wire policy | Accepted — out of scope |
| ADR-004 | unseat via client JWT discard | Accepted — REQ-05 / REQ-02 / REQ-09 |

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout / JWT / packages | read — Wave0a exception via Accepted ADR-001 |
| `fail-fast.mdc` | denial / no silent fallback | read — empty name refuse; indist. not-found |
| `http-api-conventions.mdc` | body/query/path | read — establish body models; dissolve path identity |
| `repository-pattern.mdc` | repo boundary | read — `app/db/repositories` under ADR-001 |
| `pydantic-schemas.mdc` | schemas | read — `app/models` under ADR-001 |
| `testing-verify-flows.mdc` | verify vs pytest | read — FF-01 / P15 |
| `python-tooling.mdc` | make check | read — incremental `make check` in W0 |
| `database-migrations.mdc` | Alembic scripts | read — Wave0a uses `app/db/migrations/` (no `create_postgres_migration.sh` in this repo) |
| `dependency-injection.mdc` | injector | skipped — ADR-001 retains FastAPI Depends |
| `infra-services.mdc` | pools/clients | skipped — no new infra client |
| `logging-loguru.mdc` | logging | skipped — NFR observability N/A as kill criterion |
| others | — | skipped — not in INIT-004 TASK touch set |

### P15 overlap check (recorded)

| Query | Result | Disposition |
|-------|--------|-------------|
| `PYTHONPATH=prayog-skills:. python3 prayog-skills/scripts/verify_coverage_query.py tests/verify --dump` | `error: not a directory: tests/verify` | **New** live verify FILEs warranted (FF-01 / AF-1) |
| `--capability CAP-01` / `CAP-02` / `CAP-03` | same — dir absent | **New** fixture packs under `tests/fixtures/` warranted |
| `--journey J-01` / `J-03` / `J-04` / `J-07` | same — dir absent | **New** journey fixture packs warranted |

---

## 1. Requirements (REQ) — product ids

| ID | Summary | Spec path | Waves |
|----|---------|-----------|-------|
| REQ-01 | Establish private membership→tag follow edge by name | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |
| REQ-02 | Refuse establish while unseated | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |
| REQ-03 | Inspect owner outgoing edges with name fidelity | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0, W1 |
| REQ-04 | Dissolve owned outgoing edge | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-05 | Persist edges across unseat/reseat | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-06 | Empty own-list after last dissolve | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-07 | Peer opacity on outgoing edges | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-08 | Refuse peer dissolve | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-09 | Deny list/unfollow while unseated | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0, W1 |
| REQ-10 | Missing/non-owned unfollow → indist. not-found | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-11 | Refuse empty/whitespace tag name | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |
| REQ-12 | Public tag-lane independent of edges | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-13 | Re-establish after dissolve | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-14 | Subscription-stream independent of tag edges | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-15 | Distinct from parked search memory | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-16 | Peer/guest public lane unaffected by owner edges | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-17 | Concurrent same-tag edges independent | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-18 | Refuse inbound followers-of-tag disclosure | `docs/specification/product/INIT-REALWORLD-004-api.md` | W1 |
| REQ-19 | Allow establish to corpus-empty tag name | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |
| REQ-20 | Idempotent re-follow of already-edged name | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |
| REQ-21 | Newest-established-first list order | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |
| REQ-22 | Trim + case-sensitive tag-name identity | `docs/specification/product/INIT-REALWORLD-004-api.md` | W0 |

---

## 2. Implementation phases

### Phase W0 — Followed-tags persistence + establish/list + CAP-01 prove + harness

**GOAL-W0:** Land dedicated `followed_tags` table and establish/list stewardship under Accepted ADR-001 (`app/`); refuse empty/whitespace; corpus-empty allowed; idempotent re-follow; trim + case-sensitive identity; newest-first list; unseated establish deny; co-ship `make check`, live verify drivers, and fixtures for CAP-01.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W0-01 | Add Makefile `check` target and `tests/README.md` feature map pointing at live modules (not coverage SSOT) | REQ-01 | — | `Makefile` modify; `tests/README.md` create | `make check` exits 0 on clean tree | command / `make check` | exit 0 | Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `make check` | python-tooling incremental | ADR-001 | feature/INIT-REALWORLD-004-w0-tag-follow-establish |
| TASK-W0-02 | Alembic revision for `followed_tags` table + query table descriptor | REQ-01, REQ-03, REQ-05 | TASK-W0-01 | `app/db/migrations/versions/d4e8f1a29c70_add_followed_tags_table.py` create; `app/db/queries/tables.py` modify | Migration upgrade creates `followed_tags` with `user_id` FK CASCADE, `tag_name`, `created_at`, UNIQUE/`PK` `(user_id, tag_name)`; **no** FK to public `tags` | review / TDD §8 persistence shape vs revision file | revision file present; columns match TDD §8 | Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | database-migrations Wave0a path | ADR-001; TDD E-01/E-05 | feature/INIT-REALWORLD-004-w0-tag-follow-establish |
| TASK-W0-03 | Domain/schemas + `FollowedTagsRepository` establish/list + aiosql | REQ-01, REQ-03, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22 | TASK-W0-02 | `app/models/domain/followed_tags.py` create; `app/models/schemas/followed_tags.py` create; `app/db/repositories/followed_tags.py` create; `app/db/queries/sql/followed_tags.sql` create; `tests/test_db/test_repositories/test_followed_tags.py` create | Create trims outer whitespace, refuses empty-after-trim, stores case-sensitive name, allows corpus-empty names, idempotent re-follow keeps one row, list is owner-only newest-first (`created_at DESC, tag_name ASC`) | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; create/list assertions green | Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | repository-pattern; pydantic under ADR-001 | TDD E-01/E-03/E-05/E-06/E-07 | feature/INIT-REALWORLD-004-w0-tag-follow-establish |
| TASK-W0-04 | Mount `/followed-tags` establish+list routes with seat gate; unit route coverage | REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22 | TASK-W0-03 | `app/api/routes/followed_tags.py` create; `app/api/routes/api.py` modify; `tests/test_api/test_routes/test_followed_tags.py` create | Seated establish returns success with normalized tag name once; empty/whitespace → validation refuse; unseated establish/list → auth deny; own list 200 with name fidelity + newest-first; re-follow idempotent | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; route assertions green | Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-04 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | http-api-conventions; fail-fast | ADR-001; TDD E-02 | feature/INIT-REALWORLD-004-w0-tag-follow-establish |
| TASK-W0-05 | Co-ship CAP-01 live verify + fixtures with `prayog:covers` | REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22 | TASK-W0-04 | `tests/verify/__init__.py` create; `tests/verify/verify_wave0_followed_tags_establish.py` create; `tests/fixtures/cap-01-tag-follow-establish/stimulus.json` create; `tests/fixtures/cap-01-tag-follow-establish/expected.json` create; `tests/fixtures/cap-01-tag-follow-establish/cleanup.md` create; `tests/fixtures/j-01-follow-list/stimulus.json` create; `tests/fixtures/j-02-corpus-empty/stimulus.json` create; `tests/fixtures/j-03-own-list/stimulus.json` create; `tests/fixtures/j-07-unseated-establish-deny/stimulus.json` create; `tests/fixtures/j-11-empty-name-refuse/stimulus.json` create | Script declares `prayog:covers:` including CAP-01, CAP-03, J-01, J-02, J-03, J-07, J-11; exits 0 against local compose | command / `poetry run python -m tests.verify.verify_wave0_followed_tags_establish` | exit 0; PASS markers | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run python -m tests.verify.verify_wave0_followed_tags_establish` | testing-verify-flows | ADR-001 | feature/INIT-REALWORLD-004-w0-tag-follow-establish |

#### Files (W0)

| ID | Path | Action |
|----|------|--------|
| FILE-W0-01 | `Makefile` | modify |
| FILE-W0-02 | `tests/README.md` | create |
| FILE-W0-03 | `app/db/migrations/versions/d4e8f1a29c70_add_followed_tags_table.py` | create |
| FILE-W0-04 | `app/db/queries/tables.py` | modify |
| FILE-W0-05 | `app/models/domain/followed_tags.py` | create |
| FILE-W0-06 | `app/models/schemas/followed_tags.py` | create |
| FILE-W0-07 | `app/db/repositories/followed_tags.py` | create |
| FILE-W0-08 | `app/db/queries/sql/followed_tags.sql` | create |
| FILE-W0-09 | `tests/test_db/test_repositories/test_followed_tags.py` | create |
| FILE-W0-10 | `app/api/routes/followed_tags.py` | create |
| FILE-W0-11 | `app/api/routes/api.py` | modify |
| FILE-W0-12 | `tests/test_api/test_routes/test_followed_tags.py` | create |
| FILE-W0-13 | `tests/verify/__init__.py` | create |
| FILE-W0-14 | `tests/verify/verify_wave0_followed_tags_establish.py` | create |
| FILE-W0-15 | `tests/fixtures/cap-01-tag-follow-establish/stimulus.json` | create |
| FILE-W0-16 | `tests/fixtures/cap-01-tag-follow-establish/expected.json` | create |
| FILE-W0-17 | `tests/fixtures/cap-01-tag-follow-establish/cleanup.md` | create |
| FILE-W0-18 | `tests/fixtures/j-01-follow-list/stimulus.json` | create |
| FILE-W0-19 | `tests/fixtures/j-02-corpus-empty/stimulus.json` | create |
| FILE-W0-20 | `tests/fixtures/j-03-own-list/stimulus.json` | create |
| FILE-W0-21 | `tests/fixtures/j-07-unseated-establish-deny/stimulus.json` | create |
| FILE-W0-22 | `tests/fixtures/j-11-empty-name-refuse/stimulus.json` | create |

#### Tests (W0)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W0-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-01..03, REQ-09, REQ-11, REQ-19..22 / TASK-W0-03..04 |
| TEST-W0-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres via existing async fixtures — boundary: asyncpg / `followed_tags` table) | REQ-01..03, REQ-19..22 |
| TEST-W0-L | live (smoke) | `poetry run python -m tests.verify.verify_wave0_followed_tags_establish` | CAP-01 / J-01, J-02, J-03, J-11 |

#### Verification Coverage (W0)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-01 establish | CAP-01 / J-01 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-02 unseated establish deny | CAP-03 / J-07 (establish half) | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | full J-07 in W1 |
| REQ-03 own list fidelity | CAP-02 / J-03 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | dissolve in W1 |
| REQ-09 unseated list deny | CAP-03 / J-07 (list half) | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | unfollow half in W1 |
| REQ-11 empty/whitespace refuse | CAP-01 / J-11 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-19 corpus-empty establish | CAP-01 / J-02 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-20 idempotent re-follow | CAP-01 / J-01 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-21 newest-first | CAP-02 / J-03 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-22 trim + case-sensitive | CAP-01 / J-01, J-11 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |

#### Live-verification intent (W0)

| Field | Value |
|-------|-------|
| Applicable | yes — new product surface + new `tests/verify` |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-01, CAP-03 (establish/list-deny half) / J-01, J-02, J-03, J-07 (establish/list half), J-11 |
| Fixture packs | `tests/fixtures/cap-01-tag-follow-establish/`, `tests/fixtures/j-01-follow-list/`, `tests/fixtures/j-02-corpus-empty/`, `tests/fixtures/j-03-own-list/`, `tests/fixtures/j-07-unseated-establish-deny/`, `tests/fixtures/j-11-empty-name-refuse/` |
| Runtime head binding | Bound at `wave-acceptance` against the wave PR head under test (not filled at planning) |
| Prerequisites / dependencies | Postgres up; API reachable via realworld-local compose; `followed_tags` migration applied |
| Safe test data | Synthetic users/edges only — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave0_followed_tags_establish` |
| Expected observations | Script exit 0; establish PASS; corpus-empty PASS; empty name refused; unseated establish/list denied; own list name fidelity + newest-first |
| Human look-ats | API JSON establish response shows normalized tag once; list membership matches owned edges only |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic users/edges per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

### Phase W1 — Dissolve/isolation/durability/non-composition + CAP-02/03 prove + as-built

**GOAL-W1:** Complete dissolve stewardship, peer/unseated isolation, missing/non-owned 404 polarity, reseat durability, non-composition with public lanes / subscription stream / parks, concurrent same-tag independence, no inbound followers-of-tag route; co-ship CAP-02/CAP-03 live prove; seed as-built detail + index pointer.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W1-01 | Dissolve route/repo; empty after last dissolve; re-establish after dissolve | REQ-03, REQ-04, REQ-06, REQ-13 | — | `app/api/routes/followed_tags.py` modify; `app/db/repositories/followed_tags.py` modify; `app/db/queries/sql/followed_tags.sql` modify; `app/models/schemas/followed_tags.py` modify; `tests/test_api/test_routes/test_followed_tags.py` modify; `tests/test_db/test_repositories/test_followed_tags.py` modify | Seated DELETE removes tag from own list; last dissolve → 200 empty list; dissolve then establish restores name once | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; dissolve/empty/re-establish assertions | Wave-Execution-INIT-REALWORLD-004-W1.md § TASK-W1-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast; http-api-conventions | TDD E-02/E-04 | feature/INIT-REALWORLD-004-w1-tag-follow-stewardship |
| TASK-W1-02 | Peer opacity + peer dissolve 404 + unseated list/unfollow 401 + missing/non-owned indist. 404; no inbound route | REQ-07, REQ-08, REQ-09, REQ-10, REQ-18 | TASK-W1-01 | `app/api/routes/followed_tags.py` modify; `app/db/repositories/followed_tags.py` modify; `tests/test_api/test_routes/test_followed_tags.py` modify | Peer list never includes foreign edges; peer dissolve HTTP 404 (not 403/profiles-400); unseated list/unfollow 401; missing name 404; no followers-of-tag route mounted | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; isolation assertions | Wave-Execution-INIT-REALWORLD-004-W1.md § TASK-W1-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | TDD E-04; contrast profiles 400 / comments 403 | feature/INIT-REALWORLD-004-w1-tag-follow-stewardship |
| TASK-W1-03 | Durability across JWT discard + reseat; concurrent same-tag independence | REQ-05, REQ-17 | TASK-W1-02 | `tests/test_api/test_routes/test_followed_tags.py` modify | After follow → omit bearer → re-login, own list still returns same tag; two owners following same tag remain independent after one unfollows | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; reseat + concurrent assertions | Wave-Execution-INIT-REALWORLD-004-W1.md § TASK-W1-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | ADR-004 | feature/INIT-REALWORLD-004-w1-tag-follow-stewardship |
| TASK-W1-04 | Non-composition with public tags/feed/parks + co-ship CAP-02/CAP-03 live verify + fixtures; seed as-built detail + index pointer | REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-12, REQ-13, REQ-14, REQ-15, REQ-16, REQ-17, REQ-18 | TASK-W1-03 | `tests/verify/verify_wave1_followed_tags_stewardship.py` create; `tests/fixtures/cap-02-tag-follow-stewardship/stimulus.json` create; `tests/fixtures/cap-02-tag-follow-stewardship/expected.json` create; `tests/fixtures/cap-02-tag-follow-stewardship/cleanup.md` create; `tests/fixtures/cap-03-tag-follow-isolation/stimulus.json` create; `tests/fixtures/cap-03-tag-follow-isolation/expected.json` create; `tests/fixtures/cap-03-tag-follow-isolation/cleanup.md` create; `tests/fixtures/j-04-unfollow/stimulus.json` create; `tests/fixtures/j-05-public-lane-unpersonalized/stimulus.json` create; `tests/fixtures/j-06-peer-opacity/stimulus.json` create; `tests/fixtures/j-07-unseated-deny/stimulus.json` create; `tests/fixtures/j-08-reseat-persist/stimulus.json` create; `tests/fixtures/j-09-peer-dissolve/stimulus.json` create; `tests/fixtures/j-10-empty-after-dissolve/stimulus.json` create; `tests/fixtures/j-12-missing-unfollow/stimulus.json` create; `tests/fixtures/j-13-reestablish/stimulus.json` create; `tests/fixtures/j-14-stream-noncomposition/stimulus.json` create; `tests/fixtures/j-15-parks-separation/stimulus.json` create; `tests/fixtures/j-16-peer-lane-ungated/stimulus.json` create; `tests/fixtures/j-17-concurrent-same-tag/stimulus.json` create; `tests/fixtures/j-18-no-inbound-followers/stimulus.json` create; `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-004.md` create; `docs/specification/as-built/implementation-status.md` create; `tests/README.md` modify | Live verify exits 0 with CAP-02/CAP-03 covers; public `GET /tags` + feed membership unchanged vs pre-follow baseline; as-built detail + index pointer exist | command / `poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship` | exit 0; as-built files present | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-004-api.md` | `poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship` | testing-verify-flows; SDD as-built | ADR-001/004 | feature/INIT-REALWORLD-004-w1-tag-follow-stewardship |

#### Files (W1)

| ID | Path | Action |
|----|------|--------|
| FILE-W1-01 | `app/api/routes/followed_tags.py` | modify |
| FILE-W1-02 | `app/db/repositories/followed_tags.py` | modify |
| FILE-W1-03 | `app/db/queries/sql/followed_tags.sql` | modify |
| FILE-W1-04 | `app/models/schemas/followed_tags.py` | modify |
| FILE-W1-05 | `tests/test_api/test_routes/test_followed_tags.py` | modify |
| FILE-W1-06 | `tests/test_db/test_repositories/test_followed_tags.py` | modify |
| FILE-W1-07 | `tests/verify/verify_wave1_followed_tags_stewardship.py` | create |
| FILE-W1-08 | `tests/fixtures/cap-02-tag-follow-stewardship/stimulus.json` | create |
| FILE-W1-09 | `tests/fixtures/cap-02-tag-follow-stewardship/expected.json` | create |
| FILE-W1-10 | `tests/fixtures/cap-02-tag-follow-stewardship/cleanup.md` | create |
| FILE-W1-11 | `tests/fixtures/cap-03-tag-follow-isolation/stimulus.json` | create |
| FILE-W1-12 | `tests/fixtures/cap-03-tag-follow-isolation/expected.json` | create |
| FILE-W1-13 | `tests/fixtures/cap-03-tag-follow-isolation/cleanup.md` | create |
| FILE-W1-14 | `tests/fixtures/j-04-unfollow/stimulus.json` | create |
| FILE-W1-15 | `tests/fixtures/j-05-public-lane-unpersonalized/stimulus.json` | create |
| FILE-W1-16 | `tests/fixtures/j-06-peer-opacity/stimulus.json` | create |
| FILE-W1-17 | `tests/fixtures/j-07-unseated-deny/stimulus.json` | create |
| FILE-W1-18 | `tests/fixtures/j-08-reseat-persist/stimulus.json` | create |
| FILE-W1-19 | `tests/fixtures/j-09-peer-dissolve/stimulus.json` | create |
| FILE-W1-20 | `tests/fixtures/j-10-empty-after-dissolve/stimulus.json` | create |
| FILE-W1-21 | `tests/fixtures/j-12-missing-unfollow/stimulus.json` | create |
| FILE-W1-22 | `tests/fixtures/j-13-reestablish/stimulus.json` | create |
| FILE-W1-23 | `tests/fixtures/j-14-stream-noncomposition/stimulus.json` | create |
| FILE-W1-24 | `tests/fixtures/j-15-parks-separation/stimulus.json` | create |
| FILE-W1-25 | `tests/fixtures/j-16-peer-lane-ungated/stimulus.json` | create |
| FILE-W1-26 | `tests/fixtures/j-17-concurrent-same-tag/stimulus.json` | create |
| FILE-W1-27 | `tests/fixtures/j-18-no-inbound-followers/stimulus.json` | create |
| FILE-W1-28 | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-004.md` | create |
| FILE-W1-29 | `docs/specification/as-built/implementation-status.md` | create |
| FILE-W1-30 | `tests/README.md` | modify |

#### Tests (W1)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W1-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-03..10, REQ-12..18 / TASK-W1-01..03 |
| TEST-W1-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres — boundary: followed_tags ownership + timestamps; public tags/feed untouched) | REQ-04..18 |
| TEST-W1-L | live (smoke) | `poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship` | CAP-02, CAP-03 / J-04..J-10, J-12..J-18 |

#### Verification Coverage (W1)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-04/06 dissolve + empty | CAP-02 / J-04, J-10 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-05 reseat persistence | CAP-02 / J-08 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | ADR-004 |
| REQ-07/08 peer isolation | CAP-03 / J-06, J-09 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-09 unseated list/unfollow | CAP-03 / J-07 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-10 missing/non-owned 404 | CAP-03 / J-12 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | no profiles 400 / comments 403 |
| REQ-12/16 public lane non-rewrite | CAP-03 / J-05, J-16 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-13 re-establish | CAP-01/CAP-02 / J-13 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-14 stream non-composition | CAP-03 / J-14 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-15 parks separation | CAP-02 / J-15 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | if parks absent, live asserts list is tag-names-only + no park table write |
| REQ-17 concurrent independence | CAP-03 / J-17 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-18 no inbound followers | CAP-03 / J-18 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | absence of route |

#### Live-verification intent (W1)

| Field | Value |
|-------|-------|
| Applicable | yes — material CAP-02/CAP-03 surface + new live module |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-02, CAP-03 / J-04, J-05, J-06, J-07, J-08, J-09, J-10, J-12, J-13, J-14, J-15, J-16, J-17, J-18 |
| Fixture packs | `tests/fixtures/cap-02-tag-follow-stewardship/`, `tests/fixtures/cap-03-tag-follow-isolation/`, journey packs `j-04`..`j-10`, `j-12`..`j-18` listed in Files |
| Runtime head binding | Bound at `wave-acceptance` (not planning) |
| Prerequisites / dependencies | W0 green; Postgres up; API via realworld-local compose; optional parks surface for full J-15 when present |
| Safe test data | Synthetic users/edges — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship` |
| Expected observations | Dissolve/empty/re-establish PASS; peer opacity; unseated denials; reseat keeps tag; missing unfollow 404; public lane/feed unchanged; no inbound followers route; concurrent independence |
| Human look-ats | Peer dissolve status 404 (not 403); public tag lane membership identical pre/post follow for peer/guest; OpenAPI/routes show no followers-of-tag |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic data per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

## 3. Dependencies (DEP)

| ID | Dependency | Blocks |
|----|------------|--------|
| DEP-01 | W0 followed_tags table + establish/list + CAP-01 prove | W1 stewardship/isolation prove |
| DEP-02 | `realworld-local` compose up for live smoke | W0/W1 wave-acceptance human prove |
| DEP-03 | INIT-REALWORLD-001 seat/bulletin baseline in force (not reopened) | All CAP-01..03 REQs |
| DEP-04 | Accepted ADR-001 (`app/` chassis) | All code TASKs |
| DEP-05 | Accepted ADR-004 (JWT discard unseat) | TASK-W1-03 / REQ-05 |
| DEP-06 | INIT-002 author-follow feed residual (do not rewrite) | REQ-14 live non-composition |
| DEP-07 | INIT-003 parks surface when present (optional for full J-15) | REQ-15 full dual-object prove |

---

## 4. Risks (RISK)

| ID | Risk | Mitigation |
|----|------|------------|
| RISK-01 | Tag-follow slips into `followers_to_followings` / profiles follow helpers | Dedicated `followed_tags` table + TASK ADR/MDC notes; unit asserts no author-follow write |
| RISK-02 | Peer harvest via 403 / profiles-style 400 that discloses existence | TDD E-04 — owner-scoped get → `EntityDoesNotExist` → 404 only; unit + live J-12 |
| RISK-03 | Session-only memory if edges not persisted | Dedicated Postgres table + live J-08; ADR-004 unseat does not wipe rows |
| RISK-04 | Accidental composition with public tag personalization or author feed | REQ-12/14/16/18 prove paths; leave `articles.sql` / `tags.py` untouched |
| RISK-05 | As-built absent → false “live” maturity claims | Seed as-built in W1 same PR as CAP-02/03 prove (P9) |
| RISK-06 | Chassis/MDC tension (`src/` vs `app/`) | Cite Accepted ADR-001; no INIT-004 migrate |
| RISK-07 | Alembic apply forgotten before live prove | Live prerequisites require followed_tags migration applied; stop if schema missing |
| RISK-08 | Eng ceilings (≤64 chars / ≤100 edges) invent product CAP numbers | Document as validation-only; not CAP/REQ product caps (IM-04) |

---

## 5. Out of scope

- `realworld-web` settings / any UI for tag-follow stewardship
- `realworld-local` compose product CAP ownership beyond prove environment
- Feed personalization / ranking by followed tags
- Public who-follows-this-tag social proof / inbound reverse index
- Treating tag-follow as author-follow or composing subscription ∩ tag discovery
- Reopening INIT-REALWORLD-001 favorites / public tag-lane REQs
- Reopening INIT-REALWORLD-002 author subscription / stream REQs
- Reopening INIT-REALWORLD-003 parked search REQs
- Viewer-relative following CTA on public tags (IM-07)
- Owner-visible history of former follows (IM-08)
- Comments, OAuth, email verification, mobile/native clients
- Admin tooling over other members’ edges
- Platform `src/` migrate (ADR-001)
- New INIT-004 ADRs (feasibility `new_adr: false`)

---

## 6. As-built and docs tasks

> Update these in the **same PR** as the code they describe.

| Task | File | Action |
|------|------|--------|
| Create/update per-initiative as-built detail | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-004.md` | Record W1 capability/code/test/verify detail — **KEEP** |
| Update as-built index row | `docs/specification/as-built/implementation-status.md` | Overwrite this capability’s one row in place (pointer) — never append a new table |
| Ensure live-verify coverage marker | `tests/verify/verify_wave0_followed_tags_establish.py` / `tests/verify/verify_wave1_followed_tags_stewardship.py` | Self-declare `prayog:covers:` — **do not** treat `tests/README.md` as coverage SSOT |

> **ADR lifecycle** — Draft and Accepted ADR files are created and accepted during
> `/spec-technical-review` and the `technical-review-approval` checkpoint.
> Planning consumes Accepted files only; do not add ADR promotion tasks here.

---

## 7. Plan check summary

| Check | Status |
|-------|--------|
| P1 | PASS — REQ-01..22 in §1; each wave cites via TASK Implements |
| P2 | PASS — every REQ has ≥1 TASK; every TASK Implements ≥1 REQ-* |
| P3 | PASS — every TASK has FILE paths |
| P4 | PASS — observable exit criteria + proof + expected + evidence_expected |
| P5 | PASS — unit / integration(Postgres) / smoke layers; Verification Coverage tables |
| P6 | PASS — scope bounded to INIT-004-api provider REQs |
| P7 | PASS — FF-01..03 addressed in TDD/plan; ops risks in RISK with mitigations |
| P8 | PASS — W0 → W1; DEP table |
| P9 | PASS — as-built detail + index in W1 FILE list |
| P10 | PASS — self-contained; digests; commands; live prerequisites |
| P11 | PASS — MDC notes; ADR-001 chassis exception |
| P12 | PASS — zero ADR_REQUIRED; constraining ADR-001/004 Accepted + cited |
| P13 | PASS — TDD Accepted; PE sign-off complete; zero ADR_REQUIRED; constraining ADR-001/004 fields false; structure lint `--require-sources` PASS (2 sources); TDD `--tdd` PASS; prior-INIT digest verify Should-fix (source pack unavailable) |
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
Branch:   chore/INIT-REALWORLD-004-spec-realworld-api  (Draft PR — open via Forge if absent)
PR title: "[INIT-REALWORLD-004] Spec — realworld-api"
PR body:  link meta PRD PR #12; paste §1 Requirements table + wave goals summary

Required reviewers: @drivestream-lab/backend-devs
Review deadline: 2026-11-17

PE checklist (before spec-lgtm):
  [ ] Spec + feasibility + TDD + Accepted ADRs (none new) + this plan on current head
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
| Workflow outcome | `pass` — P1–P16 PASS; sources CURRENT; Accepted TDD; zero NEW-ADR; plan ready for coding-readiness |
| Verdict | GATE OPEN REQUEST |
| Spec PR | none yet — open Draft via Forge `/commit-workspace` then `/open-draft-pr` onto `chore/INIT-REALWORLD-004-spec-realworld-api` |
| Spec PR head SHA | unbound until Forge publish |
| Gate label (current) | `spec-pending` |
| Gate label (target) | `spec-lgtm` |
| Local plan path | `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-004.md` |
| Forge readiness | fill `handoff.forge` for `/commit-workspace` onto `chore/INIT-REALWORLD-004-spec-realworld-api` — do not commit inside this skill |
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
initiative: INIT-REALWORLD-004
spec_pr_head_sha: {SHA after Forge publish}
meta_pr_head_sha: 02c74d94cf8748c1cd53a268035a8a84433caf94
impact_map_revision: 1
prd_digest: sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3
scope_digest: sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5
plan_digest: sha256:f8071600c636cc1f5ac4b6fb760aba108444ac0dd19af3ad75488e0c0ef25c82
artifacts:
  - docs/specification/product/INIT-REALWORLD-004-api.md
  - docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-004.md
  - docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md
  - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-004.md
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

initiative: INIT-REALWORLD-004
metadata:
  title: INIT-REALWORLD-004 — Private membership→tag follow edges
  summary: |
    Provider plan for CAP-01..CAP-03: owner-private establish/list/dissolve of
    membership→tag follow edges with durability across reseat, peer/unseated
    isolation, anti-reciprocity, and non-composition under the Accepted
    ADR-001 app/ chassis, with co-shipped live prove.
  playbook:
    - docs/specification/product/INIT-REALWORLD-004-api.md
    - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-004.md

target:
  org: drivestream-lab
  project: RealWorld

defaults:
  initiative: INIT-REALWORLD-004
  parent: EPIC
  labels:
    - INIT-REALWORLD-004

epic:
  id: EPIC
  repo: realworld-api
  title: "[feature] INIT-REALWORLD-004 — Private membership→tag follow edges"
  codebase: realworld-api
  spec_path: docs/specification/product/INIT-REALWORLD-004-api.md
  verify_command: poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship
  body: |
    ## Objective

    Give seated members durable owner-private membership→tag follow edges on
    realworld-api: establish, inspect with name fidelity, and dissolve — with
    fail-closed isolation from guests, post-logout actors, and peers, and no
    inbound followers-of-tag disclosure.

    ## Waves

    | Wave | Goal |
    |------|------|
    | W0 | Followed-tags persistence + establish/list + CAP-01 prove + harness |
    | W1 | Dissolve/isolation/durability/non-composition + CAP-02/03 prove + as-built |

    ## References

    - Spec: docs/specification/product/INIT-REALWORLD-004-api.md
    - Implementation plan: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-004.md
    - Technical review: docs/specification/reports/Technical-Review-INIT-REALWORLD-004.md

work:
  - id: W0
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-004 W0] Followed-tags persistence + establish/list + CAP-01 prove + harness"
    depends_on: []
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-004-api.md
    verify_command: poetry run python -m tests.verify.verify_wave0_followed_tags_establish
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
            - "make check exits 0 on a clean tree after the check target is added"
          proof:
            kind: command
            command: make check
            expected: "exit 0"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-01"
      - id: TASK-W0-02
        implements: [REQ-01, REQ-03, REQ-05]
        depends_on: [TASK-W0-01]
        files:
          - path: app/db/migrations/versions/d4e8f1a29c70_add_followed_tags_table.py
            action: create
          - path: app/db/queries/tables.py
            action: modify
        exit:
          criteria:
            - "Alembic revision defines followed_tags with user_id FK CASCADE, tag_name, created_at, UNIQUE or PK on (user_id, tag_name), and no FK to public tags"
          proof:
            kind: review
            review: "Compare app/db/migrations/versions/d4e8f1a29c70_add_followed_tags_table.py to TDD §8 persistence shape"
            expected: "columns and constraints match TDD persistence shape"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-02"
      - id: TASK-W0-03
        implements: [REQ-01, REQ-03, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22]
        depends_on: [TASK-W0-02]
        files:
          - path: app/models/domain/followed_tags.py
            action: create
          - path: app/models/schemas/followed_tags.py
            action: create
          - path: app/db/repositories/followed_tags.py
            action: create
          - path: app/db/queries/sql/followed_tags.sql
            action: create
          - path: tests/test_db/test_repositories/test_followed_tags.py
            action: create
        exit:
          criteria:
            - "Repository establish/list trims identity, refuses empty-after-trim, allows corpus-empty names, keeps idempotent single row, and returns owner-only newest-first lists"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; create/list assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-03"
      - id: TASK-W0-04
        implements: [REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22]
        depends_on: [TASK-W0-03]
        files:
          - path: app/api/routes/followed_tags.py
            action: create
          - path: app/api/routes/api.py
            action: modify
          - path: tests/test_api/test_routes/test_followed_tags.py
            action: create
        exit:
          criteria:
            - "Seated establish/list return expected statuses and fields; empty name refused; unseated establish/list denied; re-follow remains a single edge"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; route assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W0.md § TASK-W0-04"
      - id: TASK-W0-05
        implements: [REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22]
        depends_on: [TASK-W0-04]
        files:
          - path: tests/verify/__init__.py
            action: create
          - path: tests/verify/verify_wave0_followed_tags_establish.py
            action: create
          - path: tests/fixtures/cap-01-tag-follow-establish/stimulus.json
            action: create
          - path: tests/fixtures/cap-01-tag-follow-establish/expected.json
            action: create
          - path: tests/fixtures/cap-01-tag-follow-establish/cleanup.md
            action: create
          - path: tests/fixtures/j-01-follow-list/stimulus.json
            action: create
          - path: tests/fixtures/j-02-corpus-empty/stimulus.json
            action: create
          - path: tests/fixtures/j-03-own-list/stimulus.json
            action: create
          - path: tests/fixtures/j-07-unseated-establish-deny/stimulus.json
            action: create
          - path: tests/fixtures/j-11-empty-name-refuse/stimulus.json
            action: create
        exit:
          criteria:
            - "Live verify script exits 0 with prayog:covers including CAP-01 and CAP-03 establish/list-deny"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave0_followed_tags_establish
            expected: "exit 0; PASS markers for CAP-01 and unseated establish/list deny"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave0_followed_tags_establish
        covers: [CAP-01, CAP-03, J-01, J-02, J-03, J-07, J-11, REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-01-tag-follow-establish/
          - tests/fixtures/j-01-follow-list/
          - tests/fixtures/j-02-corpus-empty/
          - tests/fixtures/j-03-own-list/
          - tests/fixtures/j-07-unseated-establish-deny/
          - tests/fixtures/j-11-empty-name-refuse/
        prerequisites:
          - "compose up; followed_tags migration applied; synthetic users available"
        safe_test_data:
          - "synthetic users and tag-follow edges — no prod mutation"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave0_followed_tags_establish"
        expected_observations:
          - "Establish PASS; corpus-empty PASS; empty name refused; unseated establish/list denied; own list name fidelity + newest-first"
        human_observations:
          - locus: "API JSON establish + list for synthetic owner"
            expect: "normalized tag appears once; list contains only owner edges"
            covers: [CAP-01, J-01, J-03]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic users/edges per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Followed-tags persistence + establish/list + CAP-01 prove + harness

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W0-01 | REQ-01 | — | make check exits 0 | command/make check |
      | TASK-W0-02 | REQ-01, REQ-03, REQ-05 | TASK-W0-01 | followed_tags revision matches TDD §8 | review |
      | TASK-W0-03 | REQ-01, REQ-03, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22 | TASK-W0-02 | repo establish/list fidelity + refuse empty | command/pytest |
      | TASK-W0-04 | REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22 | TASK-W0-03 | routes establish/list + unseated deny | command/pytest |
      | TASK-W0-05 | REQ-01, REQ-02, REQ-03, REQ-09, REQ-11, REQ-19, REQ-20, REQ-21, REQ-22 | TASK-W0-04 | live CAP-01 exits 0 | command/verify_wave0_followed_tags_establish |

      ## Done when

      - [ ] All W0 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-004-api.md

  - id: W1
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-004 W1] Dissolve/isolation/durability/non-composition + CAP-02/03 prove + as-built"
    depends_on:
      - W0
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-004-api.md
    verify_command: poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship
    tasks:
      - id: TASK-W1-01
        implements: [REQ-03, REQ-04, REQ-06, REQ-13]
        depends_on: []
        files:
          - path: app/api/routes/followed_tags.py
            action: modify
          - path: app/db/repositories/followed_tags.py
            action: modify
          - path: app/db/queries/sql/followed_tags.sql
            action: modify
          - path: app/models/schemas/followed_tags.py
            action: modify
          - path: tests/test_api/test_routes/test_followed_tags.py
            action: modify
          - path: tests/test_db/test_repositories/test_followed_tags.py
            action: modify
        exit:
          criteria:
            - "Seated dissolve removes the tag; last dissolve yields HTTP 200 empty list; re-establish after dissolve restores the name once"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; dissolve/empty/re-establish assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W1.md § TASK-W1-01"
      - id: TASK-W1-02
        implements: [REQ-07, REQ-08, REQ-09, REQ-10, REQ-18]
        depends_on: [TASK-W1-01]
        files:
          - path: app/api/routes/followed_tags.py
            action: modify
          - path: app/db/repositories/followed_tags.py
            action: modify
          - path: tests/test_api/test_routes/test_followed_tags.py
            action: modify
        exit:
          criteria:
            - "Peer opacity holds; peer dissolve and missing name return HTTP 404; unseated list/unfollow return 401; no inbound followers-of-tag route exists"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; isolation assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W1.md § TASK-W1-02"
      - id: TASK-W1-03
        implements: [REQ-05, REQ-17]
        depends_on: [TASK-W1-02]
        files:
          - path: tests/test_api/test_routes/test_followed_tags.py
            action: modify
        exit:
          criteria:
            - "After follow, omit-bearer unseat, and reseat login, own list still returns the same tag name; concurrent same-tag edges stay independent after one owner unfollows"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; reseat and concurrent assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-004-W1.md § TASK-W1-03"
      - id: TASK-W1-04
        implements: [REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-12, REQ-13, REQ-14, REQ-15, REQ-16, REQ-17, REQ-18]
        depends_on: [TASK-W1-03]
        files:
          - path: tests/verify/verify_wave1_followed_tags_stewardship.py
            action: create
          - path: tests/fixtures/cap-02-tag-follow-stewardship/stimulus.json
            action: create
          - path: tests/fixtures/cap-02-tag-follow-stewardship/expected.json
            action: create
          - path: tests/fixtures/cap-02-tag-follow-stewardship/cleanup.md
            action: create
          - path: tests/fixtures/cap-03-tag-follow-isolation/stimulus.json
            action: create
          - path: tests/fixtures/cap-03-tag-follow-isolation/expected.json
            action: create
          - path: tests/fixtures/cap-03-tag-follow-isolation/cleanup.md
            action: create
          - path: tests/fixtures/j-04-unfollow/stimulus.json
            action: create
          - path: tests/fixtures/j-05-public-lane-unpersonalized/stimulus.json
            action: create
          - path: tests/fixtures/j-06-peer-opacity/stimulus.json
            action: create
          - path: tests/fixtures/j-07-unseated-deny/stimulus.json
            action: create
          - path: tests/fixtures/j-08-reseat-persist/stimulus.json
            action: create
          - path: tests/fixtures/j-09-peer-dissolve/stimulus.json
            action: create
          - path: tests/fixtures/j-10-empty-after-dissolve/stimulus.json
            action: create
          - path: tests/fixtures/j-12-missing-unfollow/stimulus.json
            action: create
          - path: tests/fixtures/j-13-reestablish/stimulus.json
            action: create
          - path: tests/fixtures/j-14-stream-noncomposition/stimulus.json
            action: create
          - path: tests/fixtures/j-15-parks-separation/stimulus.json
            action: create
          - path: tests/fixtures/j-16-peer-lane-ungated/stimulus.json
            action: create
          - path: tests/fixtures/j-17-concurrent-same-tag/stimulus.json
            action: create
          - path: tests/fixtures/j-18-no-inbound-followers/stimulus.json
            action: create
          - path: docs/specification/as-built/Implementation-Status-INIT-REALWORLD-004.md
            action: create
          - path: docs/specification/as-built/implementation-status.md
            action: create
          - path: tests/README.md
            action: modify
        exit:
          criteria:
            - "Live verify exits 0 with CAP-02 and CAP-03 covers; as-built detail and index pointer files exist"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship
            expected: "exit 0; as-built files present"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship
        covers: [CAP-02, CAP-03, J-04, J-05, J-06, J-07, J-08, J-09, J-10, J-12, J-13, J-14, J-15, J-16, J-17, J-18, REQ-04, REQ-05, REQ-07, REQ-10, REQ-12, REQ-18]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
          - W0 followed-tags surface green
        fixtures:
          - tests/fixtures/cap-02-tag-follow-stewardship/
          - tests/fixtures/cap-03-tag-follow-isolation/
          - tests/fixtures/j-04-unfollow/
          - tests/fixtures/j-05-public-lane-unpersonalized/
          - tests/fixtures/j-06-peer-opacity/
          - tests/fixtures/j-07-unseated-deny/
          - tests/fixtures/j-08-reseat-persist/
          - tests/fixtures/j-09-peer-dissolve/
          - tests/fixtures/j-10-empty-after-dissolve/
          - tests/fixtures/j-12-missing-unfollow/
          - tests/fixtures/j-13-reestablish/
          - tests/fixtures/j-14-stream-noncomposition/
          - tests/fixtures/j-15-parks-separation/
          - tests/fixtures/j-16-peer-lane-ungated/
          - tests/fixtures/j-17-concurrent-same-tag/
          - tests/fixtures/j-18-no-inbound-followers/
        prerequisites:
          - "W0 accepted; compose up; followed_tags migration applied"
        safe_test_data:
          - "synthetic users and tag-follow edges — no prod mutation"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave1_followed_tags_stewardship"
        expected_observations:
          - "Dissolve/empty/re-establish PASS; peer opacity; unseated denials; reseat keeps tag; missing unfollow 404; public lane/feed unchanged; no inbound followers"
        human_observations:
          - locus: "API JSON peer dissolve + public tag lane + route catalog"
            expect: "peer dissolve 404 not 403; public lane membership unchanged for peer/guest; no followers-of-tag route"
            covers: [CAP-02, CAP-03, J-09, J-16, J-18]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic data per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Dissolve/isolation/durability/non-composition + CAP-02/03 prove + as-built

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W1-01 | REQ-03, REQ-04, REQ-06, REQ-13 | — | dissolve/empty/re-establish | command/pytest |
      | TASK-W1-02 | REQ-07, REQ-08, REQ-09, REQ-10, REQ-18 | TASK-W1-01 | peer/unseated/missing isolation + no inbound | command/pytest |
      | TASK-W1-03 | REQ-05, REQ-17 | TASK-W1-02 | reseat + concurrent independence | command/pytest |
      | TASK-W1-04 | REQ-03..10, REQ-12..18 | TASK-W1-03 | live CAP-02/03 + as-built | command/verify_wave1_followed_tags_stewardship |

      ## Done when

      - [ ] All W1 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-004-api.md
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-implementation-plan
  outcome: pass
  artifact:
    path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-004.md
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3
    scope_digest: sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5
    meta_pr_approved_head: 02c74d94cf8748c1cd53a268035a8a84433caf94
    plan_digest: sha256:f8071600c636cc1f5ac4b6fb760aba108444ac0dd19af3ad75488e0c0ef25c82
    draft_spec_pr: none
    proposed_branch: chore/INIT-REALWORLD-004-spec-realworld-api
    new_adr: false
    new_adr_ids: []
    draft_adr_paths: []
    plan_waves: [W0, W1]
    p15_overlap_check: tests/verify-absent-new-files-warranted
    workmanifest_contract: pass
    outcome_rationale: P1-P16 PASS; Accepted TDD; zero NEW-ADR; CURRENT H1-H3/G1; plan ready for coding-readiness
  next_candidates:
    - coding-readiness
  human_checkpoint: true
  external_action: false
  forge:
    action: commit_workspace
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-004] Spec — realworld-api (implementation plan)"
    body_path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-004.md
    target_branch: chore/INIT-REALWORLD-004-spec-realworld-api
```
