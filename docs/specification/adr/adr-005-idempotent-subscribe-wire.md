# ADR-005 — Idempotent same-state subscribe wire

| Field | Value |
|-------|-------|
| Status | Accepted |
| Initiative | INIT-REALWORLD-002 |
| Feasibility finding | FF-01 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md` |
| Source spec | `docs/specification/product/INIT-REALWORLD-002-api.md` |
| Source spec digest | `sha256:b6d9a028486a5f94c6e4f5d42bd539584ed35091d5b71f7f8665f5fb47b79b4a` |
| product_constraints | `[REQ-23, REQ-07]` |
| changes_user_visible_behavior | `false` |
| spec_amendment_required | `false` |
| supersedes | none |
| superseded_by | none |
| Decision owner | PE |
| Approval evidence | Buzz `accept tdd-adr` |
| Approved head | `93cedca068c2940e034d06d6b1ba24bcfbc3beda` |
| Lint evidence | `Lint evidence: adr_boundary_lint.py 5/5, PASS, sha256:7fc921cfa52e6cf035acfa44fbfa27da9bb0a527e953a9d9c157916196f67dfa` |

## Product decisions excluded

- See REQ-23.
- See REQ-07.
- Unsubscribe same-state HTTP polarity is out of this ADR (TDD §9 keeps Conduit 400 until a REQ locks otherwise).
- Self-target and missing-author denial paths remain under REQ-10 / REQ-12.

## Context

`follow_for_user` in `app/api/routes/profiles.py` raises HTTP 400 when `profile.following` is already true (`USER_IS_ALREADY_FOLLOWED`). Unit `test_user_can_not_change_following_state_to_the_same_twice` asserts that polarity for POST. Feasibility FF-01 posed Conduit 400 vs success-no-op for duplicate mutate; only the subscribe half is bound by approved product_constraints. CTR-02 needs one POST outcome before plan TASKs touch that branch. Chassis stays under Accepted ADR-001 (`app/`). Primary bind: REQ-23.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A — Keep Conduit HTTP 400 when already following | Existing POST unit polarity stays green; Conduit tutorial fidelity | Distinct error path on no-op subscribe |
| B — HTTP 200, skip followers write, return current `following: true` | Single success envelope for first and repeat POST; graph unchanged | Invert duplicate-subscribe unit; diverge from Conduit error tutorial |

Grounding: no dormant idempotent subscribe handler — only the 400 branch. Option B is not foreclosed by code. Unsubscribe DELETE same-state is not decided here (see Product decisions excluded).

## Recommendation

Select **Option B** for POST subscribe only. When the seated caller already follows the target, skip `add_user_into_followers`, leave the edge unchanged, and return HTTP 200 with `following: true`. Keep self-target and missing-author failures on existing fail-closed paths. Adjacent bind: REQ-07.

## Consequences

- Plan TASKs remove only the already-following `HTTPException` in `follow_for_user` and invert the duplicate-subscribe unit case.
- CTR-02 verify asserts success + `following: true` on repeat subscribe.
- Unsubscribe-when-not-following remains HTTP 400 until TDD §9 or a later REQ revisits it.
- Persistence across unseat remains ADR-004; this ADR does not touch logout.

## Revisit triggers

- An approved REQ amendment requires a distinct same-state subscribe error code.
- An approved REQ locks unsubscribe same-state polarity (then supersede or add a sibling ADR).
- Consumer OpenAPI locks Conduit 400 as mandatory for duplicate follow POST.

## Lifecycle — Accepted immutability and supersession

Once `Status: Accepted`, do **not** rewrite the accepted body in place.
To change the decision:

1. create a new ADR that `supersedes` this one,
2. set this ADR's `superseded_by` to the new id and status `Superseded`,
3. record owner, date, and review evidence on both files.

## Acceptance finalization

After PE review comments are resolved and PE explicitly states the decision is
ready for acceptance — **and** product-boundary fields remain `false` —
update Status/Approval evidence/Approved head, then paste Lint evidence from
`adr_boundary_lint.py --print-evidence`.
