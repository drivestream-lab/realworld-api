---
goal: INIT-REALWORLD-003 — implementation plan
initiative: INIT-REALWORLD-003
status: Planned
date_created: 2026-11-12
source_spec: docs/specification/product/INIT-REALWORLD-003-api.md
feasibility_report: docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md
technical_review: docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md
prd_digest: sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8
impact_map: realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-003.md
impact_map_revision: 1
repo_scope_digest: sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7
approved_meta_pr_head: abfbbcff877a83c298776fd4801b8ac4c75ddfba
branch: chore/INIT-REALWORLD-003-spec-realworld-api
review_deadline: 2026-11-17
deciders: PE — spec-lgtm + Approve on exact head after full package
---

# Implementation plan — INIT-REALWORLD-003

## Source freshness and command contract

| Item | Value | Status |
|------|-------|--------|
| Spec | `docs/specification/product/INIT-REALWORLD-003-api.md` | CURRENT — live digest `sha256:37ab4aeedbdb73440a00ea968545b6c15fe5e2fc51727e961844184f9568a1bd` matches TDD citation; H1 PRD digest matches meta PRD |
| Feasibility report | `docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md` | CURRENT — same H1/H2/H3/G1; tip continuous into Accepted TDD (`new_adr: false`) |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md` | CURRENT — `Status: Accepted`; ADR_REQUIRED 0; Q-08 + E-01..E-06 resolved TDD_ONLY |
| Impact map / revision | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-003.md` / `1` | CURRENT |
| Repo scope digest | `sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7` | CURRENT — api row CAP-01..CAP-03 |
| Approved meta PR head | `abfbbcff877a83c298776fd4801b8ac4c75ddfba` | CURRENT — meta PR #10 |
| `check_command` | `make check` | RESOLVED — W0 co-ships Makefile `check` target (`poetry run black --check app tests`); ADR-001 allows incremental tooling vs full pyright/import-linter |
| `test_command` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | RESOLVED |
| `verify_command` | Wave-scoped live modules under `tests/verify/` (W0 `poetry run python -m tests.verify.verify_wave0_park_create`; W1 `poetry run python -m tests.verify.verify_wave1_park_stewardship`) | RESOLVED — co-shipped with product surface (P15); not unit |
| `ground_command` | N/A — as-built seeded in W1; `/ground-spec` after wave-acceptance (FF-02 / AF-2) | N/A — reason recorded |

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md` |
| Technical review status | Accepted |
| PE sign-off | [x] complete — 2026-11-12 (TDD `Status: Accepted`; zero ADR_REQUIRED; light-confirmation TDD under ADR-001/004) |
| Resolved ADRs | none required — light confirmation, zero NEW-ADR findings. Constraining baseline: [`adr-001-wave0a-package-chassis.md`](../adr/adr-001-wave0a-package-chassis.md) (Accepted — continue `app/`); [`adr-004-wave0a-unseat-token-discard.md`](../adr/adr-004-wave0a-unseat-token-discard.md) (Accepted — unseat = client JWT discard; park rows survive reseat). ADR-002/003/005/006 independent (favorites / favoritesCount / subscribe / Guest following). |
| ADR product-boundary re-check | Zero ADR_REQUIRED — no new ADR lint targets. Constraining ADR-001 and ADR-004: `changes_user_visible_behavior: false` / `spec_amendment_required: false` confirmed by file read at plan time (2026-11-12). |
| Outstanding PM questions | none — Q-01..Q-07 resolved via Impact-Map defaults into REQ-* |
| Outstanding domain questions | none — all resolved |

> Do not start W0 implementation until PE sign-off is marked complete above.

### ADR pass (pre-T2)

| ADR id | Domain matched | Status |
|--------|----------------|--------|
| ADR-001 | package chassis / `app/` vs `src/` | Accepted — continue (Q-08 / FF-04) |
| ADR-002 | private-shelf `favorited=` authorization | Accepted — out of INIT-003 CAP scope |
| ADR-003 | `favoritesCount` wire policy | Accepted — out of scope |
| ADR-004 | unseat via client JWT discard | Accepted — REQ-08 / REQ-12 |
| ADR-005 | idempotent subscribe wire | Accepted — out of scope |
| ADR-006 | Guest `following` omit | Accepted — out of scope |

### MDC pass (pre-T2)

| MDC file | Domain covered | Read / skipped |
|----------|----------------|----------------|
| `architecture.mdc` | Layout / JWT / packages | read — Wave0a exception via Accepted ADR-001 |
| `fail-fast.mdc` | denial / no silent fallback | read — empty query refuse; indist. not-found |
| `http-api-conventions.mdc` | body/query/path | read — park/relabel body models |
| `repository-pattern.mdc` | repo boundary | read — `app/db/repositories` under ADR-001 |
| `pydantic-schemas.mdc` | schemas | read — `app/models` under ADR-001 |
| `testing-verify-flows.mdc` | verify vs pytest | read — FF-01 / P15 |
| `python-tooling.mdc` | make check | read — incremental `make check` in W0 |
| `database-migrations.mdc` | Alembic scripts | read — Wave0a uses `app/db/migrations/` (no `create_postgres_migration.sh` in this repo) |
| `dependency-injection.mdc` | injector | skipped — ADR-001 retains FastAPI Depends |
| `infra-services.mdc` | pools/clients | skipped — no new infra client |
| `logging-loguru.mdc` | logging | skipped — NFR observability N/A as kill criterion |
| others | — | skipped — not in INIT-003 TASK touch set |

### P15 overlap check (recorded)

| Query | Result | Disposition |
|-------|--------|-------------|
| `PYTHONPATH=prayog-skills:. python3 prayog-skills/scripts/verify_coverage_query.py tests/verify --dump` | `error: not a directory: tests/verify` | **New** live verify FILEs warranted (FF-01 / AF-1) |
| `--capability CAP-01` / `CAP-02` / `CAP-03` | same — dir absent | **New** fixture packs under `tests/fixtures/` warranted |
| `--journey J-01` / `J-03` / `J-07` / `J-08` | same — dir absent | **New** journey fixture packs warranted |

---

## 1. Requirements (REQ) — product ids

| ID | Summary | Spec path | Waves |
|----|---------|-----------|-------|
| REQ-01 | Park with mnemonic label | `docs/specification/product/INIT-REALWORLD-003-api.md` | W0 |
| REQ-02 | Park without / blank label → no label | `docs/specification/product/INIT-REALWORLD-003-api.md` | W0 |
| REQ-03 | Refuse empty/whitespace query park | `docs/specification/product/INIT-REALWORLD-003-api.md` | W0 |
| REQ-04 | Refuse park while unseated | `docs/specification/product/INIT-REALWORLD-003-api.md` | W0 |
| REQ-05 | Own-recall with query fidelity | `docs/specification/product/INIT-REALWORLD-003-api.md` | W0, W1 |
| REQ-06 | Relabel owned park (incl. clear-to-none) | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-07 | Discard owned park | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-08 | Persist parks across unseat/reseat | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-09 | Empty own-recall after last discard | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-10 | Peer opacity of parks | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-11 | Refuse peer relabel/discard | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-12 | Deny list/relabel/discard while unseated | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-13 | Missing/non-owned mutate → indist. not-found | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-14 | Owner recall newest-first by park time | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |
| REQ-15 | Duplicate queries / non-unique labels allowed | `docs/specification/product/INIT-REALWORLD-003-api.md` | W0 |
| REQ-16 | Parked query string immutable after park | `docs/specification/product/INIT-REALWORLD-003-api.md` | W1 |

---

## 2. Implementation phases

### Phase W0 — Parks persistence + park/list + CAP-01 prove + harness

**GOAL-W0:** Land dedicated `parks` table and create/list stewardship under Accepted ADR-001 (`app/`); refuse empty/whitespace parks; optional/blank label → null; duplicates allowed; unseated park denied; co-ship `make check`, live verify drivers, and fixtures for CAP-01.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W0-01 | Add Makefile `check` target and `tests/README.md` feature map pointing at live modules (not coverage SSOT) | REQ-01 | — | `Makefile` modify; `tests/README.md` create | `make check` exits 0 on clean tree | command / `make check` | exit 0 | Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `make check` | python-tooling incremental | ADR-001 | feature/INIT-REALWORLD-003-w0-park-create |
| TASK-W0-02 | Alembic revision for `parks` table + query table descriptor | REQ-01, REQ-05, REQ-08 | TASK-W0-01 | `app/db/migrations/versions/b7e4c91a2f03_add_parks_table.py` create; `app/db/queries/tables.py` modify | Migration upgrade creates `parks` with `id`, `owner_id` FK CASCADE, `query_text`, nullable `label`, `created_at`, `updated_at`; no unique on query/label | review / TDD §8 persistence shape vs revision file | revision file present; columns match TDD §8 | Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | database-migrations Wave0a path | ADR-001; TDD E-01 | feature/INIT-REALWORLD-003-w0-park-create |
| TASK-W0-03 | Domain/schemas + `ParksRepository` create/list + aiosql | REQ-01, REQ-02, REQ-03, REQ-05, REQ-15 | TASK-W0-02 | `app/models/domain/parks.py` create; `app/models/schemas/parks.py` create; `app/db/repositories/parks.py` create; `app/db/queries/sql/parks.sql` create; `tests/test_db/test_repositories/test_parks.py` create | Create stores exact query + label-or-null; blank label → null; empty/whitespace query refused before insert; list returns owner-only rows; duplicate queries insert as distinct rows | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; create/list assertions green | Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | repository-pattern; pydantic under ADR-001 | TDD E-01/E-03/E-05 | feature/INIT-REALWORLD-003-w0-park-create |
| TASK-W0-04 | Mount `/parks` create+list routes with seat gate; unit route coverage | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-15 | TASK-W0-03 | `app/api/routes/parks.py` create; `app/api/routes/api.py` modify; `app/api/dependencies/parks.py` create; `tests/test_api/test_routes/test_parks.py` create | Seated create 201 with query/label fidelity; unlabeled/blank-label parks; empty query 422; unseated create 401; own list 200 with exact retained query; duplicates both listed | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; route assertions green | Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-04 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | http-api-conventions; fail-fast | ADR-001; TDD E-02 | feature/INIT-REALWORLD-003-w0-park-create |
| TASK-W0-05 | Co-ship CAP-01 live verify + fixtures with `prayog:covers` | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-15 | TASK-W0-04 | `tests/verify/__init__.py` create; `tests/verify/verify_wave0_park_create.py` create; `tests/fixtures/cap-01-park-create/stimulus.json` create; `tests/fixtures/cap-01-park-create/expected.json` create; `tests/fixtures/cap-01-park-create/cleanup.md` create; `tests/fixtures/j-01-labeled-park/stimulus.json` create; `tests/fixtures/j-02-unlabeled-park/stimulus.json` create; `tests/fixtures/j-12-empty-query-refuse/stimulus.json` create; `tests/fixtures/j-03-own-recall-list/stimulus.json` create | Script declares `prayog:covers:` including CAP-01, J-01, J-02, J-03, J-12; exits 0 against local compose | command / `poetry run python -m tests.verify.verify_wave0_park_create` | exit 0; PASS markers | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run python -m tests.verify.verify_wave0_park_create` | testing-verify-flows | ADR-001 | feature/INIT-REALWORLD-003-w0-park-create |

#### Files (W0)

| ID | Path | Action |
|----|------|--------|
| FILE-W0-01 | `Makefile` | modify |
| FILE-W0-02 | `tests/README.md` | create |
| FILE-W0-03 | `app/db/migrations/versions/b7e4c91a2f03_add_parks_table.py` | create |
| FILE-W0-04 | `app/db/queries/tables.py` | modify |
| FILE-W0-05 | `app/models/domain/parks.py` | create |
| FILE-W0-06 | `app/models/schemas/parks.py` | create |
| FILE-W0-07 | `app/db/repositories/parks.py` | create |
| FILE-W0-08 | `app/db/queries/sql/parks.sql` | create |
| FILE-W0-09 | `tests/test_db/test_repositories/test_parks.py` | create |
| FILE-W0-10 | `app/api/routes/parks.py` | create |
| FILE-W0-11 | `app/api/routes/api.py` | modify |
| FILE-W0-12 | `app/api/dependencies/parks.py` | create |
| FILE-W0-13 | `tests/test_api/test_routes/test_parks.py` | create |
| FILE-W0-14 | `tests/verify/__init__.py` | create |
| FILE-W0-15 | `tests/verify/verify_wave0_park_create.py` | create |
| FILE-W0-16 | `tests/fixtures/cap-01-park-create/stimulus.json` | create |
| FILE-W0-17 | `tests/fixtures/cap-01-park-create/expected.json` | create |
| FILE-W0-18 | `tests/fixtures/cap-01-park-create/cleanup.md` | create |
| FILE-W0-19 | `tests/fixtures/j-01-labeled-park/stimulus.json` | create |
| FILE-W0-20 | `tests/fixtures/j-02-unlabeled-park/stimulus.json` | create |
| FILE-W0-21 | `tests/fixtures/j-12-empty-query-refuse/stimulus.json` | create |
| FILE-W0-22 | `tests/fixtures/j-03-own-recall-list/stimulus.json` | create |

#### Tests (W0)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W0-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-01..05, REQ-15 / TASK-W0-03..04 |
| TEST-W0-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres via existing async fixtures — boundary: asyncpg / `parks` table) | REQ-01..05, REQ-15 |
| TEST-W0-L | live (smoke) | `poetry run python -m tests.verify.verify_wave0_park_create` | CAP-01 / J-01, J-02, J-03, J-12 |

#### Verification Coverage (W0)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-01 labeled park | CAP-01 / J-01 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-02 unlabeled / blank label | CAP-01 / J-02 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-03 empty/whitespace refuse | CAP-01 / J-12 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |
| REQ-04 unseated park deny | CAP-03 / J-07 (park half) | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | full J-07 in W1 |
| REQ-05 own list fidelity | CAP-02 / J-03 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | stewardship mutate in W1 |
| REQ-15 duplicates allowed | CAP-01 / J-01 | TEST-W0-U | TEST-W0-I | TEST-W0-L | N/A | |

#### Live-verification intent (W0)

| Field | Value |
|-------|-------|
| Applicable | yes — new product surface + new `tests/verify` |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-01 / J-01, J-02, J-03, J-12 |
| Fixture packs | `tests/fixtures/cap-01-park-create/`, `tests/fixtures/j-01-labeled-park/`, `tests/fixtures/j-02-unlabeled-park/`, `tests/fixtures/j-12-empty-query-refuse/`, `tests/fixtures/j-03-own-recall-list/` |
| Runtime head binding | Bound at `wave-acceptance` against the wave PR head under test (not filled at planning) |
| Prerequisites / dependencies | Postgres up; API reachable via realworld-local compose; parks migration applied |
| Safe test data | Synthetic users/parks only — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave0_park_create` |
| Expected observations | Script exit 0; labeled/unlabeled park PASS; empty query refused; unseated create 401; own list query fidelity |
| Human look-ats | API JSON create response shows exact query + label-or-null; list membership matches owned parks only |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic users/parks per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

### Phase W1 — Relabel/discard/isolation/durability + CAP-02/03 prove + as-built

**GOAL-W1:** Complete stewardship mutate paths (relabel incl. clear, discard), newest-first ordering, query immutability, peer/unseated isolation, missing/non-owned 404 polarity, reseat durability; co-ship CAP-02/CAP-03 live prove; seed as-built detail + index pointer.

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W1-01 | Relabel (incl. clear) + discard routes/repo; query column immutable; newest-first list; empty after last discard | REQ-05, REQ-06, REQ-07, REQ-09, REQ-14, REQ-16 | — | `app/api/routes/parks.py` modify; `app/api/dependencies/parks.py` modify; `app/db/repositories/parks.py` modify; `app/db/queries/sql/parks.sql` modify; `app/models/schemas/parks.py` modify; `tests/test_api/test_routes/test_parks.py` modify; `tests/test_db/test_repositories/test_parks.py` modify | Relabel updates/clears label only; query unchanged; discard removes from list; last discard → 200 `[]`; list `ORDER BY created_at DESC, id DESC` | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; mutate/order/empty assertions | Wave-Execution-INIT-REALWORLD-003-W1.md § TASK-W1-01 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast; http-api-conventions | TDD E-04/E-05/E-06 | feature/INIT-REALWORLD-003-w1-park-stewardship |
| TASK-W1-02 | Peer opacity + peer mutate 404 + unseated list/relabel/discard 401 + missing/non-owned indist. 404 | REQ-10, REQ-11, REQ-12, REQ-13 | TASK-W1-01 | `app/api/dependencies/parks.py` modify; `app/db/repositories/parks.py` modify; `tests/test_api/test_routes/test_parks.py` modify | Peer list never includes foreign parks; peer mutate HTTP 404 (not 403); unseated list/mutate 401; missing id 404; own recall unchanged | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; isolation assertions | Wave-Execution-INIT-REALWORLD-003-W1.md § TASK-W1-02 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | TDD E-04; contrast comments 403 | feature/INIT-REALWORLD-003-w1-park-stewardship |
| TASK-W1-03 | Durability across JWT discard + reseat | REQ-08 | TASK-W1-02 | `tests/test_api/test_routes/test_parks.py` modify | After park → omit bearer → re-login, own list still returns same `query_text` | command / `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | exit 0; reseat assertion | Wave-Execution-INIT-REALWORLD-003-W1.md § TASK-W1-03 | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | fail-fast | ADR-004 | feature/INIT-REALWORLD-003-w1-park-stewardship |
| TASK-W1-04 | Co-ship CAP-02/CAP-03 live verify + fixtures; seed as-built detail + index pointer | REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-16 | TASK-W1-03 | `tests/verify/verify_wave1_park_stewardship.py` create; `tests/fixtures/cap-02-park-stewardship/stimulus.json` create; `tests/fixtures/cap-02-park-stewardship/expected.json` create; `tests/fixtures/cap-02-park-stewardship/cleanup.md` create; `tests/fixtures/cap-03-park-isolation/stimulus.json` create; `tests/fixtures/cap-03-park-isolation/expected.json` create; `tests/fixtures/cap-03-park-isolation/cleanup.md` create; `tests/fixtures/j-04-relabel/stimulus.json` create; `tests/fixtures/j-05-discard/stimulus.json` create; `tests/fixtures/j-06-peer-opacity/stimulus.json` create; `tests/fixtures/j-07-unseated-deny/stimulus.json` create; `tests/fixtures/j-08-reseat-persist/stimulus.json` create; `tests/fixtures/j-09-peer-mutate/stimulus.json` create; `tests/fixtures/j-10-empty-after-discard/stimulus.json` create; `tests/fixtures/j-11-missing-id/stimulus.json` create; `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-003.md` create; `docs/specification/as-built/implementation-status.md` create; `tests/README.md` modify | Live verify exits 0 with CAP-02/CAP-03 covers; as-built detail + index pointer exist | command / `poetry run python -m tests.verify.verify_wave1_park_stewardship` | exit 0; as-built files present | wave-accepted on tip | realworld-api | `docs/specification/product/INIT-REALWORLD-003-api.md` | `poetry run python -m tests.verify.verify_wave1_park_stewardship` | testing-verify-flows; SDD as-built | ADR-001/004 | feature/INIT-REALWORLD-003-w1-park-stewardship |

#### Files (W1)

| ID | Path | Action |
|----|------|--------|
| FILE-W1-01 | `app/api/routes/parks.py` | modify |
| FILE-W1-02 | `app/api/dependencies/parks.py` | modify |
| FILE-W1-03 | `app/db/repositories/parks.py` | modify |
| FILE-W1-04 | `app/db/queries/sql/parks.sql` | modify |
| FILE-W1-05 | `app/models/schemas/parks.py` | modify |
| FILE-W1-06 | `tests/test_api/test_routes/test_parks.py` | modify |
| FILE-W1-07 | `tests/test_db/test_repositories/test_parks.py` | modify |
| FILE-W1-08 | `tests/verify/verify_wave1_park_stewardship.py` | create |
| FILE-W1-09 | `tests/fixtures/cap-02-park-stewardship/stimulus.json` | create |
| FILE-W1-10 | `tests/fixtures/cap-02-park-stewardship/expected.json` | create |
| FILE-W1-11 | `tests/fixtures/cap-02-park-stewardship/cleanup.md` | create |
| FILE-W1-12 | `tests/fixtures/cap-03-park-isolation/stimulus.json` | create |
| FILE-W1-13 | `tests/fixtures/cap-03-park-isolation/expected.json` | create |
| FILE-W1-14 | `tests/fixtures/cap-03-park-isolation/cleanup.md` | create |
| FILE-W1-15 | `tests/fixtures/j-04-relabel/stimulus.json` | create |
| FILE-W1-16 | `tests/fixtures/j-05-discard/stimulus.json` | create |
| FILE-W1-17 | `tests/fixtures/j-06-peer-opacity/stimulus.json` | create |
| FILE-W1-18 | `tests/fixtures/j-07-unseated-deny/stimulus.json` | create |
| FILE-W1-19 | `tests/fixtures/j-08-reseat-persist/stimulus.json` | create |
| FILE-W1-20 | `tests/fixtures/j-09-peer-mutate/stimulus.json` | create |
| FILE-W1-21 | `tests/fixtures/j-10-empty-after-discard/stimulus.json` | create |
| FILE-W1-22 | `tests/fixtures/j-11-missing-id/stimulus.json` | create |
| FILE-W1-23 | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-003.md` | create |
| FILE-W1-24 | `docs/specification/as-built/implementation-status.md` | create |
| FILE-W1-25 | `tests/README.md` | modify |

#### Tests (W1)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W1-U | unit | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` | REQ-05..14, REQ-16 / TASK-W1-01..03 |
| TEST-W1-I | integration/contract | `poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/` (Postgres — boundary: parks ownership + timestamps) | REQ-05..14, REQ-16 |
| TEST-W1-L | live (smoke) | `poetry run python -m tests.verify.verify_wave1_park_stewardship` | CAP-02, CAP-03 / J-04..J-11 |

#### Verification Coverage (W1)

| REQ / criterion | CAP / J (live rung) | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|---------------------|------|----------------------|-------|---------|-------|
| REQ-06/16 relabel + immutable query | CAP-02 / J-04 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-07/09 discard + empty | CAP-02 / J-05, J-10 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-08 reseat persistence | CAP-02 / J-08 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | ADR-004 |
| REQ-14 newest-first | CAP-02 / J-03 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-10/11 peer isolation | CAP-03 / J-06, J-09 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-12 unseated list/mutate | CAP-03 / J-07 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | |
| REQ-13 missing/non-owned 404 | CAP-03 / J-11 | TEST-W1-U | TEST-W1-I | TEST-W1-L | N/A | no comments-style 403 |

#### Live-verification intent (W1)

| Field | Value |
|-------|-------|
| Applicable | yes — material CAP-02/CAP-03 surface + new live module |
| Environment class | local-compose (`realworld-local`) |
| Mode | smoke |
| Prove rungs | CAP-02, CAP-03 / J-04, J-05, J-06, J-07, J-08, J-09, J-10, J-11 |
| Fixture packs | `tests/fixtures/cap-02-park-stewardship/`, `tests/fixtures/cap-03-park-isolation/`, journey packs `j-04`..`j-11` listed in Files |
| Runtime head binding | Bound at `wave-acceptance` (not planning) |
| Prerequisites / dependencies | W0 green; Postgres up; API via realworld-local compose |
| Safe test data | Synthetic users/parks — no prod mutation |
| Steps / command | `poetry run python -m tests.verify.verify_wave1_park_stewardship` |
| Expected observations | Relabel/clear/discard PASS; peer opacity; unseated denials; reseat keeps query; missing id 404; empty after last discard |
| Human look-ats | Peer mutate status 404 (not 403); list order newest-first for ≥2 parks; query text unchanged after relabel |
| Expected evidence | `wave-accepted on tip` |
| Cleanup | Remove synthetic data per fixture cleanup.md |
| Stop conditions | Non-zero exit or unexpected 5xx → stop; do not start Pass-2 |

---

## 3. Dependencies (DEP)

| ID | Dependency | Blocks |
|----|------------|--------|
| DEP-01 | W0 parks table + create/list + CAP-01 prove | W1 stewardship/isolation prove |
| DEP-02 | `realworld-local` compose up for live smoke | W0/W1 wave-acceptance human prove |
| DEP-03 | INIT-REALWORLD-001 seat/bulletin baseline in force (not reopened) | All CAP-01..03 REQs |
| DEP-04 | Accepted ADR-001 (`app/` chassis) | All code TASKs |
| DEP-05 | Accepted ADR-004 (JWT discard unseat) | TASK-W1-03 / REQ-08 |

---

## 4. Risks (RISK)

| ID | Risk | Mitigation |
|----|------|------------|
| RISK-01 | Peer harvest via 403 that discloses existence | TDD E-04 — owner-scoped get → `EntityDoesNotExist` → 404 only; unit + live J-11 |
| RISK-02 | Session-only memory if parks not persisted | Dedicated Postgres table + live J-08; ADR-004 unseat does not wipe rows |
| RISK-03 | Scope creep into web UI / auto-run | Keep non-goals; prove API-only; deferred web/local |
| RISK-04 | As-built absent → false “live” maturity claims | Seed as-built in W1 same PR as CAP-02/03 prove (P9) |
| RISK-05 | Chassis/MDC tension (`src/` vs `app/`) | Cite Accepted ADR-001; no INIT-003 migrate |
| RISK-06 | Comments-style 403 copied onto parks path deps | TASK notes + unit asserting 404 for peer-owned id |
| RISK-07 | Alembic apply forgotten before live prove | Live prerequisites require parks migration applied; stop if schema missing |

---

## 5. Out of scope

- `realworld-web` settings / any UI for parked-search stewardship
- `realworld-local` compose product CAP ownership beyond prove environment
- Share / public / collaborative parks
- Auto-running parked queries against article search
- New article-search ranking / full-text product
- Label-as-unique-slot identity packaging
- Reopening INIT-REALWORLD-001 favorites/nameplate or INIT-REALWORLD-002 subscription rules
- Comments, OAuth, email verification, mobile/native clients
- Admin tooling over other members’ parks
- Platform `src/` migrate (ADR-001)
- New INIT-003 ADRs (feasibility `new_adr: false`)

---

## 6. As-built and docs tasks

> Update these in the **same PR** as the code they describe.

| Task | File | Action |
|------|------|--------|
| Create/update per-initiative as-built detail | `docs/specification/as-built/Implementation-Status-INIT-REALWORLD-003.md` | Record W1 capability/code/test/verify detail — **KEEP** |
| Update as-built index row | `docs/specification/as-built/implementation-status.md` | Overwrite this capability’s one row in place (pointer) — never append a new table |
| Ensure live-verify coverage marker | `tests/verify/verify_wave0_park_create.py` / `tests/verify/verify_wave1_park_stewardship.py` | Self-declare `prayog:covers:` — **do not** treat `tests/README.md` as coverage SSOT |

> **ADR lifecycle** — Draft and Accepted ADR files are created and accepted during
> `/spec-technical-review` and the `technical-review-approval` checkpoint.
> Planning consumes Accepted files only; do not add ADR promotion tasks here.

---

## 7. Plan check summary

| Check | Status |
|-------|--------|
| P1 | PASS — REQ-01..16 in §1; each wave cites via TASK Implements |
| P2 | PASS — every REQ has ≥1 TASK; every TASK Implements ≥1 REQ-* |
| P3 | PASS — every TASK has FILE paths |
| P4 | PASS — observable exit criteria + proof + expected + evidence_expected |
| P5 | PASS — unit / integration(Postgres) / smoke layers; Verification Coverage tables |
| P6 | PASS — scope bounded to INIT-003-api provider REQs |
| P7 | PASS — FF-01..04 addressed in TDD/plan; ops risks in RISK with mitigations |
| P8 | PASS — W0 → W1; DEP table |
| P9 | PASS — as-built detail + index in W1 FILE list |
| P10 | PASS — self-contained; digests; commands; live prerequisites |
| P11 | PASS — MDC notes; ADR-001 chassis exception |
| P12 | PASS — zero ADR_REQUIRED; constraining ADR-001/004 Accepted + cited |
| P13 | PASS — TDD Accepted; PE sign-off complete; zero NEW-ADR product-boundary lint targets; constraining ADR fields false |
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
Branch:   chore/INIT-REALWORLD-003-spec-realworld-api  (Draft PR — open via Forge if absent)
PR title: "[INIT-REALWORLD-003] Spec — realworld-api"
PR body:  link meta PRD PR #10; paste §1 Requirements table + wave goals summary

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
| Spec PR | none open yet — open Draft PR on `chore/INIT-REALWORLD-003-spec-realworld-api` via Forge before PE unlock |
| Spec PR head SHA | `{SHA after Forge publish}` |
| Gate label (current) | `spec-pending` |
| Gate label (target) | `spec-lgtm` |
| Local plan path | `docs/specification/reports/Implementation-Plan-INIT-REALWORLD-003.md` |
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
initiative: INIT-REALWORLD-003
spec_pr_head_sha: {SHA after Forge publish}
meta_pr_head_sha: abfbbcff877a83c298776fd4801b8ac4c75ddfba
impact_map_revision: 1
prd_digest: sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8
scope_digest: sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7
plan_digest: sha256:32af4a6c75992c83f96a4fab7a0999fc685edb0581f6b26e95e62fe2e7eaa2a7
artifacts:
  - docs/specification/product/INIT-REALWORLD-003-api.md
  - docs/specification/reports/Initiative-Feasibility-Report-INIT-REALWORLD-003.md
  - docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md
  - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-003.md
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

initiative: INIT-REALWORLD-003
metadata:
  title: INIT-REALWORLD-003 — Replay-ready personal search memory
  summary: |
    Provider plan for CAP-01..CAP-03: owner-private park/recall/relabel/discard
    with query-string fidelity, durability across reseat, and peer/unseated
    isolation under the Accepted ADR-001 app/ chassis, with co-shipped live prove.
  playbook:
    - docs/specification/product/INIT-REALWORLD-003-api.md
    - docs/specification/reports/Implementation-Plan-INIT-REALWORLD-003.md

target:
  org: drivestream-lab
  project: RealWorld

defaults:
  initiative: INIT-REALWORLD-003
  parent: EPIC
  labels:
    - INIT-REALWORLD-003

epic:
  id: EPIC
  repo: realworld-api
  title: "[feature] INIT-REALWORLD-003 — Replay-ready personal search memory"
  codebase: realworld-api
  spec_path: docs/specification/product/INIT-REALWORLD-003-api.md
  verify_command: poetry run python -m tests.verify.verify_wave1_park_stewardship
  body: |
    ## Objective

    Give seated members durable owner-private memory of parked search intents on
    realworld-api: park, recall with query fidelity, relabel, and discard — with
    fail-closed isolation from guests, post-logout actors, and peers.

    ## Waves

    | Wave | Goal |
    |------|------|
    | W0 | Parks persistence + park/list + CAP-01 prove + harness |
    | W1 | Relabel/discard/isolation/durability + CAP-02/03 prove + as-built |

    ## References

    - Spec: docs/specification/product/INIT-REALWORLD-003-api.md
    - Implementation plan: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-003.md
    - Technical review: docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md

work:
  - id: W0
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-003 W0] Parks persistence + park/list + CAP-01 prove + harness"
    depends_on: []
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-003-api.md
    verify_command: poetry run python -m tests.verify.verify_wave0_park_create
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
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-01"
      - id: TASK-W0-02
        implements: [REQ-01, REQ-05, REQ-08]
        depends_on: [TASK-W0-01]
        files:
          - path: app/db/migrations/versions/b7e4c91a2f03_add_parks_table.py
            action: create
          - path: app/db/queries/tables.py
            action: modify
        exit:
          criteria:
            - "Alembic revision defines parks table with owner_id FK CASCADE, query_text, nullable label, created_at/updated_at, and no unique constraint on query or label"
          proof:
            kind: review
            review: "Compare app/db/migrations/versions/b7e4c91a2f03_add_parks_table.py to TDD §8 persistence shape"
            expected: "columns and constraints match TDD persistence shape"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-02"
      - id: TASK-W0-03
        implements: [REQ-01, REQ-02, REQ-03, REQ-05, REQ-15]
        depends_on: [TASK-W0-02]
        files:
          - path: app/models/domain/parks.py
            action: create
          - path: app/models/schemas/parks.py
            action: create
          - path: app/db/repositories/parks.py
            action: create
          - path: app/db/queries/sql/parks.sql
            action: create
          - path: tests/test_db/test_repositories/test_parks.py
            action: create
        exit:
          criteria:
            - "Repository create/list preserves query fidelity, maps blank label to null, refuses empty query before insert, and allows duplicate query parks"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; create/list assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-03"
      - id: TASK-W0-04
        implements: [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-15]
        depends_on: [TASK-W0-03]
        files:
          - path: app/api/routes/parks.py
            action: create
          - path: app/api/routes/api.py
            action: modify
          - path: app/api/dependencies/parks.py
            action: create
          - path: tests/test_api/test_routes/test_parks.py
            action: create
        exit:
          criteria:
            - "Seated create/list return expected statuses and fields; empty query refused; unseated create returns 401; duplicates both appear on own list"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; route assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W0.md § TASK-W0-04"
      - id: TASK-W0-05
        implements: [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-15]
        depends_on: [TASK-W0-04]
        files:
          - path: tests/verify/__init__.py
            action: create
          - path: tests/verify/verify_wave0_park_create.py
            action: create
          - path: tests/fixtures/cap-01-park-create/stimulus.json
            action: create
          - path: tests/fixtures/cap-01-park-create/expected.json
            action: create
          - path: tests/fixtures/cap-01-park-create/cleanup.md
            action: create
          - path: tests/fixtures/j-01-labeled-park/stimulus.json
            action: create
          - path: tests/fixtures/j-02-unlabeled-park/stimulus.json
            action: create
          - path: tests/fixtures/j-12-empty-query-refuse/stimulus.json
            action: create
          - path: tests/fixtures/j-03-own-recall-list/stimulus.json
            action: create
        exit:
          criteria:
            - "Live verify script exits 0 with prayog:covers including CAP-01"
          proof:
            kind: command
            command: poetry run python -m tests.verify.verify_wave0_park_create
            expected: "exit 0; PASS markers for CAP-01"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave0_park_create
        covers: [CAP-01, J-01, J-02, J-03, J-12, REQ-01, REQ-02, REQ-03, REQ-05]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
        fixtures:
          - tests/fixtures/cap-01-park-create/
          - tests/fixtures/j-01-labeled-park/
          - tests/fixtures/j-02-unlabeled-park/
          - tests/fixtures/j-12-empty-query-refuse/
          - tests/fixtures/j-03-own-recall-list/
        prerequisites:
          - "compose up; parks migration applied; synthetic users available"
        safe_test_data:
          - "synthetic users and parks — no prod mutation"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave0_park_create"
        expected_observations:
          - "Labeled/unlabeled park PASS; empty query refused; unseated create denied; own list query fidelity"
        human_observations:
          - locus: "API JSON create + list for synthetic owner"
            expect: "exact query string retained; blank label absent/null; list contains only owner parks"
            covers: [CAP-01, J-01, J-03]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic users/parks per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Parks persistence + park/list + CAP-01 prove + harness

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W0-01 | REQ-01 | — | make check exits 0 | command/make check |
      | TASK-W0-02 | REQ-01, REQ-05, REQ-08 | TASK-W0-01 | parks table revision matches TDD §8 | review |
      | TASK-W0-03 | REQ-01, REQ-02, REQ-03, REQ-05, REQ-15 | TASK-W0-02 | repo create/list fidelity + refuse empty | command/pytest |
      | TASK-W0-04 | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-15 | TASK-W0-03 | routes create/list + unseated deny | command/pytest |
      | TASK-W0-05 | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-15 | TASK-W0-04 | live CAP-01 exits 0 | command/verify_wave0_park_create |

      ## Done when

      - [ ] All W0 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-003-api.md

  - id: W1
    kind: issue
    repo: realworld-api
    title: "[INIT-REALWORLD-003 W1] Relabel/discard/isolation/durability + CAP-02/03 prove + as-built"
    depends_on:
      - W0
    codebase: realworld-api
    spec_path: docs/specification/product/INIT-REALWORLD-003-api.md
    verify_command: poetry run python -m tests.verify.verify_wave1_park_stewardship
    tasks:
      - id: TASK-W1-01
        implements: [REQ-05, REQ-06, REQ-07, REQ-09, REQ-14, REQ-16]
        depends_on: []
        files:
          - path: app/api/routes/parks.py
            action: modify
          - path: app/api/dependencies/parks.py
            action: modify
          - path: app/db/repositories/parks.py
            action: modify
          - path: app/db/queries/sql/parks.sql
            action: modify
          - path: app/models/schemas/parks.py
            action: modify
          - path: tests/test_api/test_routes/test_parks.py
            action: modify
          - path: tests/test_db/test_repositories/test_parks.py
            action: modify
        exit:
          criteria:
            - "Relabel/clear and discard work; query immutable; newest-first list; empty list after last discard is HTTP 200"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; mutate/order/empty assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W1.md § TASK-W1-01"
      - id: TASK-W1-02
        implements: [REQ-10, REQ-11, REQ-12, REQ-13]
        depends_on: [TASK-W1-01]
        files:
          - path: app/api/dependencies/parks.py
            action: modify
          - path: app/db/repositories/parks.py
            action: modify
          - path: tests/test_api/test_routes/test_parks.py
            action: modify
        exit:
          criteria:
            - "Peer opacity holds; peer mutate and missing id return HTTP 404; unseated list/mutate return 401; own recall unchanged"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; isolation assertions green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W1.md § TASK-W1-02"
      - id: TASK-W1-03
        implements: [REQ-08]
        depends_on: [TASK-W1-02]
        files:
          - path: tests/test_api/test_routes/test_parks.py
            action: modify
        exit:
          criteria:
            - "After park, omit-bearer unseat, and reseat login, own recall still returns the same query_text"
          proof:
            kind: command
            command: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
            expected: "exit 0; reseat assertion green"
            evidence_expected: "Wave-Execution-INIT-REALWORLD-003-W1.md § TASK-W1-03"
      - id: TASK-W1-04
        implements: [REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14, REQ-16]
        depends_on: [TASK-W1-03]
        files:
          - path: tests/verify/verify_wave1_park_stewardship.py
            action: create
          - path: tests/fixtures/cap-02-park-stewardship/stimulus.json
            action: create
          - path: tests/fixtures/cap-02-park-stewardship/expected.json
            action: create
          - path: tests/fixtures/cap-02-park-stewardship/cleanup.md
            action: create
          - path: tests/fixtures/cap-03-park-isolation/stimulus.json
            action: create
          - path: tests/fixtures/cap-03-park-isolation/expected.json
            action: create
          - path: tests/fixtures/cap-03-park-isolation/cleanup.md
            action: create
          - path: tests/fixtures/j-04-relabel/stimulus.json
            action: create
          - path: tests/fixtures/j-05-discard/stimulus.json
            action: create
          - path: tests/fixtures/j-06-peer-opacity/stimulus.json
            action: create
          - path: tests/fixtures/j-07-unseated-deny/stimulus.json
            action: create
          - path: tests/fixtures/j-08-reseat-persist/stimulus.json
            action: create
          - path: tests/fixtures/j-09-peer-mutate/stimulus.json
            action: create
          - path: tests/fixtures/j-10-empty-after-discard/stimulus.json
            action: create
          - path: tests/fixtures/j-11-missing-id/stimulus.json
            action: create
          - path: docs/specification/as-built/Implementation-Status-INIT-REALWORLD-003.md
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
            command: poetry run python -m tests.verify.verify_wave1_park_stewardship
            expected: "exit 0; as-built files present"
            evidence_expected: "wave-accepted on tip"
    verification:
      check: make check
      unit: poetry run pytest tests/ -q --ignore=tests/debug/ --ignore=tests/verify/
      live:
        applicable: true
        mode: smoke
        command: poetry run python -m tests.verify.verify_wave1_park_stewardship
        covers: [CAP-02, CAP-03, J-04, J-05, J-06, J-07, J-08, J-09, J-10, J-11, REQ-06, REQ-08, REQ-10, REQ-13]
        dependencies:
          - postgres
          - realworld-api via realworld-local compose
          - W0 parks surface green
        fixtures:
          - tests/fixtures/cap-02-park-stewardship/
          - tests/fixtures/cap-03-park-isolation/
          - tests/fixtures/j-04-relabel/
          - tests/fixtures/j-05-discard/
          - tests/fixtures/j-06-peer-opacity/
          - tests/fixtures/j-07-unseated-deny/
          - tests/fixtures/j-08-reseat-persist/
          - tests/fixtures/j-09-peer-mutate/
          - tests/fixtures/j-10-empty-after-discard/
          - tests/fixtures/j-11-missing-id/
        prerequisites:
          - "W0 accepted; compose up; parks migration applied"
        safe_test_data:
          - "synthetic users and parks — no prod mutation"
        steps:
          - "Run poetry run python -m tests.verify.verify_wave1_park_stewardship"
        expected_observations:
          - "Relabel/discard PASS; peer opacity; unseated denials; reseat keeps query; missing id 404; empty after last discard"
        human_observations:
          - locus: "API JSON peer mutate + owner list order"
            expect: "peer mutate 404 not 403; newest-first order for >=2 parks; query unchanged after relabel"
            covers: [CAP-02, CAP-03, J-04, J-11]
        evidence_expected: "wave-accepted on tip"
        cleanup:
          - "Remove synthetic data per fixture cleanup.md"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      Relabel/discard/isolation/durability + CAP-02/03 prove + as-built

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W1-01 | REQ-05, REQ-06, REQ-07, REQ-09, REQ-14, REQ-16 | — | relabel/discard/order/empty | command/pytest |
      | TASK-W1-02 | REQ-10, REQ-11, REQ-12, REQ-13 | TASK-W1-01 | peer/unseated/missing isolation | command/pytest |
      | TASK-W1-03 | REQ-08 | TASK-W1-02 | reseat persistence | command/pytest |
      | TASK-W1-04 | REQ-05..14, REQ-16 | TASK-W1-03 | live CAP-02/03 + as-built | command/verify_wave1_park_stewardship |

      ## Done when

      - [ ] All W1 tasks complete per plan exit proof

      ## Spec reference

      docs/specification/product/INIT-REALWORLD-003-api.md
```

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-implementation-plan
  outcome: pass
  artifact:
    path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-003.md
    digest: sha256:32af4a6c75992c83f96a4fab7a0999fc685edb0581f6b26e95e62fe2e7eaa2a7
  blockers: []
  signals:
    source_freshness: CURRENT
    map_revision: 1
    prd_digest: sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8
    scope_digest: sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7
    meta_pr_approved_head: abfbbcff877a83c298776fd4801b8ac4c75ddfba
    plan_digest: sha256:32af4a6c75992c83f96a4fab7a0999fc685edb0581f6b26e95e62fe2e7eaa2a7
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
    title: "[INIT-REALWORLD-003] Spec — realworld-api (implementation plan)"
    body_path: docs/specification/reports/Implementation-Plan-INIT-REALWORLD-003.md
    target_branch: chore/INIT-REALWORLD-003-spec-realworld-api
```
