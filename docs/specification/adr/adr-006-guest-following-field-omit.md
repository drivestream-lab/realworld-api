# ADR-006 — Guest profile response omits `following`

| Field | Value |
|-------|-------|
| Status | Accepted |
| Initiative | INIT-REALWORLD-002 |
| Feasibility finding | FF-02 |
| Technical review | `docs/specification/reports/Technical-Review-INIT-REALWORLD-002.md` |
| Source spec | `docs/specification/product/INIT-REALWORLD-002-api.md` |
| Source spec digest | `sha256:b6d9a028486a5f94c6e4f5d42bd539584ed35091d5b71f7f8665f5fb47b79b4a` |
| product_constraints | `[REQ-22, REQ-04]` |
| changes_user_visible_behavior | `false` |
| spec_amendment_required | `false` |
| supersedes | none |
| superseded_by | none |
| Decision owner | PE |
| Approval evidence | Buzz `accept tdd-adr` |
| Approved head | `93cedca068c2940e034d06d6b1ba24bcfbc3beda` |
| Lint evidence | `Lint evidence: adr_boundary_lint.py 5/5, PASS, sha256:bf81fe7fc238bc8c595ebff37167b76b65e6b830b1d7aebd770cee9b703b17d4` |

## Product decisions excluded

- See REQ-22.
- See REQ-04.
- Seated profile boolean semantics stay under REQ-07 / REQ-08.
- Follower/following counts remain out of scope (IM-01).

## Context

`Profile` in `app/models/domain/profiles.py` declares `following: bool = False`. `ProfilesRepository.get_profile_by_username` loads the edge only when `requested_user` is present; Guests still serialize `following: false` because the default is written into JSON. Unit `test_unregistered_user_will_receive_profile_without_following` asserts falsy, not key absence. CTR-02 needs one Guest wire shape before schema TASKs. Chassis stays under Accepted ADR-001. Primary bind: REQ-22.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A — Emit `following: false` for Guests (Conduit default) | No schema change; existing guest unit stays green | Wire presents a boolean that was never edge-loaded; consumers may treat it as authoritative |
| B — Omit `following` on Guest profile responses | Key absence matches “no seated edge loaded”; seated responses keep true/false | Requires `Optional` / `exclude_none` (or response variant); invert guest unit to assert key missing |

Grounding: no alternate Guest DTO found — one `Profile` model for all callers. Option B is viable via response serialization change under `app/`.

## Recommendation

Select **Option B**. For unauthenticated profile reads, serialize without the `following` key. For seated reads, keep emitting the loaded boolean. Prefer `Optional[bool] = None` on the domain/schema model with response `exclude_none`, or an equivalent Guest response mapper — plan picks the minimal `app/models` change. Adjacent bind: REQ-04.

## Consequences

- Guest OpenAPI/examples document absent `following`; seated examples keep the boolean.
- Invert guest profile unit to assert key omission (not merely falsy).
- Article-embedded author profiles must apply the same Guest omit rule when the caller is unseated.

## Revisit triggers

- An approved REQ requires Guests to always receive an explicit false boolean.
- A later INIT splits public author DTO from seated subscription DTO permanently.

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
