# ADR-003 — Constant favoritesCount on article wire

| Field | Value |
|-------|-------|
| Status | Accepted |
| Initiative | INIT-REALWORLD-001 |
| Feasibility finding | FF-03 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-001.md` |
| Source spec | `docs/specification/product/INIT-REALWORLD-001-api.md` |
| Source spec digest | `sha256:006eb93a2b6006b9a8c0c54772f85e9c12c4de67dee3210fb3da15760b5ea360` |
| product_constraints | [REQ-25, REQ-27] |
| changes_user_visible_behavior | `false` |
| spec_amendment_required | `false` |
| supersedes | none |
| superseded_by | none |
| Decision owner | PE |
| Approval evidence | Buzz `accept tdd-adr` / god take on technical-review-approval (2026-11-11) |
| Approved head | docs/spec-init-realworld-001 (Draft spec PR tip at acceptance) |
| Lint evidence | `Lint evidence: adr_boundary_lint.py 2/2, PASS, sha256:8c47027141d5c9a816acc015aaeb270f0900e8923b774c1567c2fb1d39f8bf31` |

## Product decisions excluded

List authorization is owned elsewhere. This ADR only locks the favorites counter field on article responses.

## Context

Article serializers may emit a live favorites aggregate or a constant. Wave0a needs a single wire policy before coding to avoid cache and contract churn. Primary bind: REQ-25.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A — Retain live `favoritesCount` | Full Conduit RealWorld wire-field fidelity | Cross-caller aggregate integers remain on CTR-01/CTR-05 payloads |
| B — Constant overwrite (prefer keep-key/`0`) in response mapper | Removes live aggregate from the wire; join rows unchanged | Keep-key constant vs omit-key OpenAPI break if consumers require absence |

## Recommendation

Map favoritesCount to constant 0 on article responses for Wave0a. Adjacent bind: REQ-27.

## Consequences

- Favorite/unfavorite response builders must use the same mapper constant.
- Verify/CTR assertions treat `favoritesCount` as the mapped constant when the key is present.
- List-filter authorization remains ADR-002.

## Revisit triggers

- An approved REQ amendment changes the wire policy for this field.
- Consumer contracts require dropping the JSON key and OpenAPI is revised in a follow-on INIT.

## Lifecycle — Accepted immutability and supersession

Once `Status: Accepted`, do **not** rewrite the accepted body in place.
To change the decision:

1. create a new ADR that `supersedes` this one,
2. set this ADR's `superseded_by` to the new id and status `Superseded`,
3. record owner, date, and review evidence on both files.

## Acceptance finalization

After PE acceptance, set Status/Approval evidence/Approved head.
Lint evidence is recorded in the metadata table row above.
