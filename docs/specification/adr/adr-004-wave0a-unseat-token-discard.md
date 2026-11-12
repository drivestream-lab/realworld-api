# ADR-004 — Wave0a unseat via client JWT discard

| Field | Value |
|-------|-------|
| Status | Accepted |
| Initiative | INIT-REALWORLD-001 |
| Feasibility finding | FF-04 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md` |
| Source spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Source spec digest | `sha256:006eb93a2b6006b9a8c0c54772f85e9c12c4de67dee3210fb3da15760b5ea360` |
| product_constraints | [REQ-12, REQ-13] |
| changes_user_visible_behavior | `false` |
| spec_amendment_required | `false` |
| supersedes | none |
| superseded_by | none |
| Decision owner | PE |
| Approval evidence | Buzz `accept tdd-adr` / god take on technical-review-approval (2026-11-11) |
| Approved head | docs/spec-init-realworld-001 (Draft spec PR tip at acceptance) |
| Lint evidence | `Lint evidence: adr_boundary_lint.py 2/2, PASS, sha256:6e22d2b04315470df42880cf4efeb8c50e73b74f231bbec7e418126d21e75f41` |

## Product decisions excluded

Recovery flows and revoke-store designs are out of scope for this Wave0a record.

## Context

Ending a seated session can be client omission of the bearer or a server-side revoke path. Wave0a must pick one before auth middleware TASKs land. Primary bind: REQ-12.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A — Client omits bearer (no server revoke) | Matches baseline; no new persistence | A retained token remains valid until expiry |
| B — Server-side revocation on logout | Invalidates presented tokens server-side | New revoke store + middleware; no baseline mechanism |

## Recommendation

Choose client discard of the bearer for Wave0a unseat. Do not add a logout RPC or revoke store in this INIT. Adjacent bind: REQ-13.

## Consequences

- No logout RPC TASK is required for Wave0a.
- Protected-route prove after discard exercises omit-`Authorization` requests.
- Q-05 multi-device cascade stays deferred; sibling sessions are not revoked here.

## Revisit triggers

- An approved REQ requires immediate server invalidation of outstanding tokens.
- Idle-timeout or token-theft kill criteria reopen revoke design.

## Lifecycle — Accepted immutability and supersession

Once `Status: Accepted`, do **not** rewrite the accepted body in place.
To change the decision:

1. create a new ADR that `supersedes` this one,
2. set this ADR's `superseded_by` to the new id and status `Superseded`,
3. record owner, date, and review evidence on both files.

## Acceptance finalization

After PE acceptance, set Status/Approval evidence/Approved head.
Lint evidence is recorded in the metadata table row above.
