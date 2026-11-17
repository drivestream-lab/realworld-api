# Implementation status — INIT-REALWORLD-001

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-001 |
| Spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Repo | drivestream-lab/realworld-api |
| Updated | 2026-11-17 |
| Source | `/ground-spec` W0 (seed; W1/W2 rows fill on later grounds) |

## Wave matrix

| Wave | Goal | Assigned REQs | Code / verify | Unit | Live | human_approved | Ground report |
|------|------|---------------|---------------|------|------|----------------|---------------|
| W0 | Seat + public bulletin + feed order + prove scaffold | REQ-01..14, REQ-34 | `app/api/routes/authentication.py`; `app/api/routes/articles/articles_resource.py`; `app/db/repositories/articles.py`; `tests/verify/verify_wave0_seat_bulletin.py`; fixtures under `tests/fixtures/cap-01-bulletin/`, `cap-02-seat/`, `j-01-guest-feed/`, `j-05-register-login/` | Wave-Execution: pytest exit 0 (95 passed) | Script + fixtures co-shipped; human ran prove at wave-acceptance | yes — `wave-accepted` on PR #25 (`1b9d1c2…` accept tip; tip advanced with learning-extract) | `docs/specification/reports/Ground-Report-INIT-REALWORLD-001-W0.md` |
| W1 | Tagged publish + own revise/delete | REQ-15..24 | not yet | — | — | no | — |
| W2 | Private shelf + nameplate + as-built complete | REQ-25..33, REQ-35 | not yet | — | — | no | — |

## Capability detail (W0 live)

| Capability | Status | Entry points | Evidence |
|------------|--------|--------------|----------|
| CAP-01 public bulletin | implemented / unit-tested / live-verified (human accept) | `list_articles`, `retrieve_article_by_slug`, tag/author filters, guest profile | Ground-Report W0 REQ-01..07, REQ-34; verify covers |
| CAP-02 contribution seat | implemented / unit-tested / live-verified (human accept) | `register` (no seat token), `login` (seat), omit-bearer mutate deny | Ground-Report W0 REQ-08..14; verify covers |

## Notes

- Package chassis remains `app/` per ADR-001.
- Unseat is client JWT discard per ADR-004 (no logout RPC).
- Unseated mutate deny may surface as HTTP 403 (chassis APIKeyHeader) — accepted fail-closed at wave-acceptance.
- Full as-built index pointer rows for CAP-03..06 land when those waves ground; W2 plan also lists as-built FILE create — this file is the KEEP detail SSOT and is overwritten in place as later waves close.
