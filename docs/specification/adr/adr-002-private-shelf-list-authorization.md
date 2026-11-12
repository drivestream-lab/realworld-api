# ADR-002 — Owner-scoped favorited filter authorization

| Field | Value |
|-------|-------|
| Status | Accepted |
| Initiative | INIT-REALWORLD-001 |
| Feasibility finding | FF-02 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md` |
| Source spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Source spec digest | `sha256:006eb93a2b6006b9a8c0c54772f85e9c12c4de67dee3210fb3da15760b5ea360` |
| product_constraints | [REQ-25, REQ-26, REQ-27] |
| changes_user_visible_behavior | `false` |
| spec_amendment_required | `false` |
| supersedes | none |
| superseded_by | none |
| Decision owner | PE |
| Approval evidence | Buzz `accept tdd-adr` / god take on technical-review-approval (2026-11-11) |
| Approved head | docs/spec-init-realworld-001 (Draft spec PR tip at acceptance) |
| Lint evidence | `Lint evidence: adr_boundary_lint.py 2/2, PASS, sha256:50e68d173f70b855d87cc1bec0893ca7ae95627f82d24aa06452434c495bf7dd` |

## Product decisions excluded

Shelf mutation rules stay with their owning REQs; this ADR only locks list-filter authorization.

## Context

List handlers that honor a favorited-username query can leak membership across callers unless the filter is owner-scoped. Wave0a must choose fail-closed owner gating vs open joins before coding. Primary bind: REQ-27.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A — Keep unrestricted `favorited=<username>` join | Conduit compatibility; existing unit test stays green | Any caller can enumerate another username’s favorite rows |
| B — Gate join on seated caller identity match | Fail-closed query path for mismatched/missing caller | Breaks unrestricted `favorited=` usage; unit polarity must invert |

## Recommendation

Gate the favorited filter so it applies only when the seated caller matches the requested username; otherwise fail closed. Adjacent binds: REQ-25; REQ-26.

## Consequences

- `test_filtering_by_favorited` must assert mismatch/guest denial and matching-caller success.
- CTR-05 consumer calls must pass only the seated caller’s own username as `favorited` subject.
- Aggregate count emission is separate — see ADR-003.

## Revisit triggers

- An approved REQ restores unrestricted favorites-by-username listing.
- Own-shelf reads move to a dedicated authenticated resource and the query filter is removed.

## Lifecycle — Accepted immutability and supersession

Once `Status: Accepted`, do **not** rewrite the accepted body in place.
To change the decision:

1. create a new ADR that `supersedes` this one,
2. set this ADR's `superseded_by` to the new id and status `Superseded`,
3. record owner, date, and review evidence on both files.

## Acceptance finalization

After PE acceptance, set Status/Approval evidence/Approved head.
Lint evidence is recorded in the metadata table row above.
