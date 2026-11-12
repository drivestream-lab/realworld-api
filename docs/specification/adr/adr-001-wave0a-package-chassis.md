# ADR-001 — Wave0a package chassis under `app/`

| Field | Value |
|-------|-------|
| Status | Accepted |
| Initiative | INIT-REALWORLD-001 |
| Feasibility finding | FF-01 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md` |
| Source spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Source spec digest | `sha256:006eb93a2b6006b9a8c0c54772f85e9c12c4de67dee3210fb3da15760b5ea360` |
| product_constraints | [REQ-01, REQ-08, REQ-10, REQ-12, REQ-15, REQ-20, REQ-25, REQ-27, REQ-30, REQ-34] |
| changes_user_visible_behavior | `false` |
| spec_amendment_required | `false` |
| supersedes | none |
| superseded_by | none |
| Decision owner | PE |
| Approval evidence | Buzz `accept tdd-adr` / god take on technical-review-approval (2026-11-11) |
| Approved head | docs/spec-init-realworld-001 (Draft spec PR tip at acceptance) |
| Lint evidence | `Lint evidence: adr_boundary_lint.py 2/2, PASS, sha256:7ca16d679b23b1f2081b62ea858da9ee4fe7977573bd3ab24bea05a3ae89ebbd` |

## Product decisions excluded

Initiative product register stays authoritative. This record only locks the package root for TASK placement.

## Context

Wave0a must pick a package root before coding TASKs land. The live tree already executes from `app/`; platform MDC documents a different preferred root. Hardening the live root vs relocating modules is an engineering sequencing choice. Primary bind: REQ-01.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A — Retain and harden `app/` for Wave0a | TASKs map onto existing modules; matches `tests/test_*` | Explicit Wave0a exception to platform `src/` layout |
| B — Migrate onto platform `src/` in this INIT | Early MDC alignment | Full move before CAP prove; no dormant `src/` scaffold found |

## Recommendation

Select **Option A**. Keep Wave0a package root at `app/` for TASK placement under the product_constraints set (primary: REQ-01). Record an INIT-local exception to platform layout MDC. Defer any alternate package-root migration to a later INIT that supersedes this ADR.

## Consequences

- Plan TASKs name `app/**` paths.
- Tooling (`pyright`, import-linter, `make check`) may land incrementally without a package move.
- Residual mounted handlers outside Wave0a covers remain out of plan verify markers (TDD §2 / §5) — not a second chassis choice.

## Revisit triggers

- A follow-on INIT scopes platform chassis migration.
- Injector/`BaseInfraService` lifecycle becomes mandatory for a required outbound sibling client.

## Lifecycle — Accepted immutability and supersession

Once `Status: Accepted`, do **not** rewrite the accepted body in place.
To change the decision:

1. create a new ADR that `supersedes` this one,
2. set this ADR's `superseded_by` to the new id and status `Superseded`,
3. record owner, date, and review evidence on both files.

## Acceptance finalization

After PE review comments are resolved and PE explicitly states the decision is
ready for acceptance — **and** product-boundary fields remain `false` —
update Status/Approval evidence/Approved head, then re-record Lint evidence.

```text
# Paste `Lint evidence:` line from adr_boundary_lint.py --print-evidence at acceptance time.
```
