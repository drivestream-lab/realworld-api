# INIT-REALWORLD-004 — spec slice for realworld-api

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-004 |
| PRD | `realworld-meta/prd/INIT-REALWORLD-004.md` |
| PRD digest (H1) | `sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3` |
| Meta PR | https://github.com/drivestream-lab/realworld-meta/pull/12 |
| Meta PR approved head (G1) | `02c74d94cf8748c1cd53a268035a8a84433caf94` |
| Impact map | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-004.md` |
| Impact-map revision (H3) | `1` |
| Repo scope digest (H2) | `sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5` |
| Tech-lead approval | Review `PRR_kwDOVac9Rs8AAAABXCxxnw` / id `5841383839` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T11:55:48Z`; `commit_id` = `02c74d94cf8748c1cd53a268035a8a84433caf94` (matches merged meta PR #12 head; label `impact-map-lgtm`) |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Status | Draft — dev review required before Forge publish |

> **H4 citations:** The H1–H3 (and G1) rows above are the durable authority
> carrier for mid-lane freshness. Feas / TDD / plan digests are walk-time only
> and may be purged at initiative closure — see
> `prayog-skills/references/artifact-write-contract.md`.

## Overview

`realworld-api` is the **provider** for CAP-01..CAP-03 and REQ-01..REQ-22: seated owner-private membership→tag follow edges (establish / inspect outgoing / dissolve by tag name) with name fidelity on the owner outgoing list; refuse empty/whitespace tag names; durable membership retention across unseat/reseat; fail-closed unseated and peer isolation; anti-reciprocity (no inbound followers-of-tag); non-composition with INIT-002 author-follow / subscription-stream; non-application to public discovery — proven on the machine-consumable API surface (no web UI this INIT).

**Out of this repo:** Settings / any web UI for tag-follow edge stewardship (`realworld-web`); local compose/env delta for prove hosting (`realworld-local`); feed personalization; inbound who-follows-this-tag social proof; reopening INIT-REALWORLD-001 favorites / public tag-lane requirement ids, INIT-002 author-subscription / subscription-stream requirement ids, or INIT-003 parked-search requirement ids; comments; OAuth; email verification; mobile/native clients; admin tooling over other members’ edges; new infra services.

**Ownership:** this spec states observable API product behavior, acceptance, field meaning, invariants, errors, and compatibility only. Implementation architecture (persistence shape, route encoding, chassis under `app/` vs `src/`) is **not** decided here — routed to feasibility / technical review.

**Baseline:** INIT-REALWORLD-001 seat rules remain the gate for “signed-in reader.” INIT-001 favorites, INIT-002 author subscriptions, and INIT-003 parked searches are **not** reopened. Source scan finds **author** follow under `app/api/routes/profiles.py` and public tag catalog under `app/api/routes/tags.py`, but **no** membership→tag follow-edge tables or stewardship routes — this INIT introduces a new prove surface distinct from author-follow.

## Functional requirements

| ID | Requirement | PRD source | Condition / event | Observable result | Evidence layer |
|----|-------------|-----------|-------------------|-------------------|----------------|
| REQ-01 | Establish a private membership→tag follow edge by tag name | PRD REQ-01 / CAP-01 | Seated member follows a tag using a non-empty tag name (after trim per REQ-22) | An owner-private outgoing edge exists for that tag name; owner outgoing list includes that name exactly once | live (CAP-01, J-01) |
| REQ-02 | Refuse establish while unseated | PRD REQ-02 / CAP-03 | Guest or post-logout actor attempts to follow a tag | No new tag-follow edge is created for any membership | live (CAP-03, J-07) |
| REQ-03 | Inspect only the owner’s outgoing tag-follow edges with name fidelity | PRD REQ-03 / CAP-02 | Seated member requests their followed-tag list when they own zero or more outgoing edges | List contains exactly that member’s followed tag names (or empty); no other member’s edges appear; each name appears at most once | live (CAP-02, J-03) |
| REQ-04 | Dissolve an owned outgoing tag-follow edge | PRD REQ-04 / CAP-02 | Seated member unfollows a tag name they currently follow | That tag name no longer appears on the owner’s outgoing edge list | live (CAP-02, J-04) |
| REQ-05 | Persist tag-follow edges across unseat and reseat | PRD REQ-05 / CAP-02 | Seated member follows a tag, logs out, then logs in again without changing edges while unseated | After reseat, owner list still includes that tag name | live (CAP-02, J-08) |
| REQ-06 | Allow empty own-list after the last dissolve | PRD REQ-06 / CAP-02 | Seated member unfollows their last remaining followed tag | Owner outgoing edge list is empty and valid (not an error wall) | live (CAP-02, J-10) |
| REQ-07 | Keep one member’s outgoing tag-follow edges invisible to another seated member | PRD REQ-07 / CAP-03 | Member A owns ≥1 outgoing edge; Member B is seated and is not A | B cannot obtain A’s outgoing edge set via list or direct access | live (CAP-03, J-06) |
| REQ-08 | Refuse dissolve of another member’s tag-follow edge | PRD REQ-08 / CAP-03 | Seated peer attempts to unfollow a tag on Member A’s outgoing set (or otherwise remove A’s edge) | A’s outgoing edge set unchanged; peer’s own list unchanged by that attempt | live (CAP-03, J-09) |
| REQ-09 | Deny list / unfollow while unseated | PRD REQ-09 / CAP-03 | Guest or post-logout actor attempts list or unfollow | No outgoing edge contents of any member are disclosed as a successful list result; no unfollow side effects | live (CAP-03, J-07) |
| REQ-10 | Refuse unfollow of a missing or non-owned edge as indistinguishable not-found | PRD REQ-10 / CAP-03; IM-03 / OQ-03 default | Seated member attempts unfollow against a tag they do not currently follow (or a non-owned edge identity) | Own list unchanged; fail closed as indistinguishable not-found to the requester; no outgoing-edge contents disclosed | unit / live (CAP-03, J-12) |
| REQ-11 | Refuse establish of empty or whitespace-only tag name | PRD REQ-11 / CAP-01 | Seated member attempts to follow empty or whitespace-only tag name | No edge is created; owner list unchanged by that attempt | live (CAP-01, J-11) |
| REQ-12 | Keep public tag-lane membership independent of own tag-follow edges | PRD REQ-12 / CAP-03 | Seated member follows ≥1 tag then uses public tag-lane / bulletin discovery | Public discovery membership remains tag-true and unpersonalized by this INIT’s edges; guest browse unchanged | live (CAP-03, J-05) |
| REQ-13 | Allow re-establish after dissolve | PRD REQ-13 / CAP-02 | Seated member unfollows a tag they followed, then follows that same tag name again | Owner list again includes that tag name exactly once | live (CAP-02, J-13) |
| REQ-14 | Keep subscription-stream membership independent of tag-follow edges | PRD REQ-14 / CAP-03 | Seated member who holds INIT-002 author subscriptions also follows ≥1 tag | Subscription-stream membership remains driven by author subscriptions only; tag-follow edges do not add/remove stream articles this INIT | live (CAP-03, J-14) |
| REQ-15 | Keep tag-follow edges distinct from parked search memory | PRD REQ-15 / CAP-02 | Seated member who owns ≥1 INIT-003 parked search also follows ≥1 tag | Owner outgoing list lists tag names only; parked search recall remains a separate object and is not rewritten by tag follow/unfollow this INIT | live (CAP-02, J-15) |
| REQ-16 | Keep peers’ public lane browse unaffected by owner edges | PRD REQ-16 / CAP-03 | Member A follows ≥1 tag; Member B (or a guest) browses the corresponding public tag lane | Public lane membership for B/guest stays tag-true; A’s private edge does not gate, hide, or personalize that lane for others | live (CAP-03, J-16) |
| REQ-17 | Keep concurrent same-tag edges independent across members | PRD REQ-17 / CAP-03 | Member A and Member B both follow the same tag name; then A unfollows that tag | B’s outgoing list still includes that tag name; A’s no longer does; no shared/merged edge | live (CAP-03, J-17) |
| REQ-18 | Refuse inbound follower disclosure for a tag | PRD REQ-18 / CAP-03 | Any actor attempts to obtain which members follow a given tag (counts or actor list) via a product surface of this INIT | No successful disclosure of follower membership for that tag; owner-only outgoing list remains the sole follow-inspection path | live (CAP-03, J-18) |
| REQ-19 | Allow establish to a tag name with zero current article hits | PRD OQ-01 / IM-01 default; CAP-01 | Seated member follows a non-empty tag name whose public lane currently has zero articles | Edge is established; owner list includes that name; empty public lane does not block establish | live (CAP-01, J-02) |
| REQ-20 | Treat re-follow of an already-edged tag name as idempotent success | PRD OQ-02 / IM-02 default; CAP-01 | Seated member who already holds an outgoing edge for tag name T follows T again | Outgoing list still shows T exactly once; no second distinct edge; distinct conflict outcome not required | unit / live (CAP-01, J-01) |
| REQ-21 | Order owner outgoing list newest-established-first | PRD OQ-05 / IM-05 default; CAP-02 | Seated member requests own outgoing list with ≥2 edges | Edges are ordered newest-established-first; exact timestamp source left to engineering | integration / live (CAP-02, J-03) |
| REQ-22 | Identify tag-follow targets by trimmed, case-sensitive tag name | PRD OQ-06 / IM-06 default; CAP-01 / CAP-02 | Seated member establishes, lists, or dissolves using a tag name that may have outer whitespace | Outer whitespace is trimmed before identity comparison; after trim, match is case-sensitive as stored; empty-after-trim is refused (REQ-11) | unit / live (CAP-01, CAP-02, J-01, J-04, J-11) |

> **Id convention:** `REQ-*` is canonical (`prayog-skills/references/id-conventions.md`).
> Legacy display alias `FR-{nn}` ≡ `REQ-{nn}` — prefer `REQ-*`.
>
> **Behavioral acceptance vs evidence:** Condition/event + observable result are
> the product acceptance statement (implementation-neutral). Evidence layer
> names how it will be proved later. Live evidence cites `CAP-*` and/or `J-*`.

## Capabilities (carried from PRD)

| ID | Capability | Journeys | Notes |
|----|------------|----------|-------|
| CAP-01 | Establish a private membership→tag follow edge | J-01, J-02, J-08, J-11, J-13, J-17 | Seated follow by tag name; empty name refused; corpus-empty target allowed (REQ-19); idempotent re-establish (REQ-20); trim + case-sensitive identity (REQ-22) |
| CAP-02 | Inspect and dissolve own outgoing tag-follow edges | J-01, J-03, J-04, J-08, J-10, J-13, J-15, J-17 | List with name fidelity; unfollow dissolves; empty set valid; persist across reseat; re-establish after dissolve; distinct from search parks; newest-first (REQ-21) |
| CAP-03 | Follow-edge privacy, anti-reciprocity, and non-composition | J-05, J-06, J-07, J-09, J-12, J-14, J-16, J-17, J-18 | Peer opacity; unseated fail-closed; missing/non-owned dissolve denied as indistinguishable not-found (REQ-10); no inbound follower index; concurrent same-tag independence; edges do not rewrite public lanes, bulletin, subscription stream, or peer edges |

## Journeys (carried from PRD)

| ID | Actor | Trigger | Main flow | Primary edge | Abandon | Caps |
|----|-------|---------|-----------|--------------|---------|------|
| J-01 | Seated member | Wants a durable follow relationship to a topic tag | Follows tag by name → lists → sees that name once as outgoing edge target | Already-edged → idempotent (REQ-20) | Abandons before follow → no edge | CAP-01, CAP-02 |
| J-02 | Seated member | Establishes an edge to a tag with no current article hits | Follows tag name absent from corpus (REQ-19) → lists → sees name | Empty public lane still edged | — | CAP-01 |
| J-03 | Seated member | Wants to see which tags they hold outgoing edges to | Opens own followed-tag / outgoing-edge list | Empty list when none established; newest-first when ≥2 (REQ-21) | Leaves without changes | CAP-02 |
| J-04 | Seated member | No longer wants a tag edge | Unfollows tag → lists → name absent | — | — | CAP-02 |
| J-05 | Seated member | Continues public discovery after establishing edges | Follows ≥1 tag → browses public tag lanes / bulletin | Lanes stay unpersonalized | Stops browsing | CAP-03 |
| J-06 | Peer member | Tries to harvest another’s tag interests | Attempts to list/access Member A’s outgoing edges | Denied / no disclosure | — | CAP-03 |
| J-07 | Guest / post-logout | Tries stewardship without a seat | Attempts follow, list, or unfollow | Fail closed; no side effects; no disclosure | — | CAP-03 |
| J-08 | Seated member | Relies on continuity across sessions | Follows tag → logs out → logs in → lists | Same tag name still present | — | CAP-01, CAP-02 |
| J-09 | Peer member | Tries to alter another’s outgoing edges | Attempts unfollow of A’s followed tag | A unchanged | — | CAP-03 |
| J-10 | Seated member | Clears the last edge | Unfollows final tag → lists empty | Empty is valid | — | CAP-02 |
| J-11 | Seated member | Tries to establish empty name | Attempts follow with empty/whitespace name | Refused; list unchanged | — | CAP-01 |
| J-12 | Seated member | Uses a bad unfollow target | Attempts unfollow on a tag they do not follow | Fail closed; own list unchanged | — | CAP-03 |
| J-13 | Seated member | Returns to a previously dissolved edge | Unfollows tag → follows same name again → lists | Name present once after re-establish | Abandons after unfollow → stays empty for that name | CAP-01, CAP-02 |
| J-14 | Seated member | Holds author subscriptions and tag-follow edges together | Has ≥1 author subscription; follows ≥1 tag; opens subscription stream | Stream membership ignores tag-follow edges | — | CAP-03 |
| J-15 | Seated member | Holds parked searches and tag-follow edges together | Owns ≥1 INIT-003 park; follows ≥1 tag; recalls parks and outgoing list | Objects remain separate; unfollow does not clear parks | — | CAP-02 |
| J-16 | Peer / guest | Browses a public lane that the owner edged | A follows tag X; B or guest opens public lane X | Lane stays ungated and tag-true for B/guest | — | CAP-03 |
| J-17 | Two seated members | Independently follow the same tag, then one leaves | A and B both follow tag X; A unfollows X; both list | A’s list lacks X; B’s list still has X | — | CAP-01, CAP-02, CAP-03 |
| J-18 | Any actor | Tries to learn who follows a tag | Attempts inbound followers-of-tag disclosure for tag X | No successful follower membership disclosure this INIT | — | CAP-03 |

## Negative and failure paths

| REQ | Condition | Required behavior | Why it matters | Evidence |
|-----|-----------|-------------------|----------------|----------|
| REQ-03 / J-03 | Owner has zero outgoing edges | Empty list, still seated-only | Empty ≠ error; matches success “list works” | live (J-03) |
| REQ-03 | Owner has edges | Listed names match established tags; at most once each | Edge fidelity observable without UI | live (J-03) |
| REQ-02 / REQ-09 | Unseated follow/list/unfollow | Fail closed; no disclosure; no mutations | Kill assumption — seat gate | live (J-07) |
| REQ-07 / J-06 | Peer tries to read owner’s outgoing edges | Isolation holds; no interest harvest | Kill assumption — unauthorized cannot see others’ follows | live (J-06) |
| REQ-08 / J-09 | Peer tries to remove owner’s edge | Target unchanged | Isolation beyond read opacity | live (J-09) |
| REQ-06 / J-10 | Last edge dissolved | Empty own-list allowed | Prevents “must always follow one tag” false rule | live (J-10) |
| REQ-10 / J-12 | Unfollow when not following / non-owned | Indistinguishable not-found; own list unchanged; no disclosure | Prevents cross-owner leakage via guessed identities | unit / live (J-12) |
| REQ-11 / J-11 | Empty / whitespace tag name | Establish refused; no record | Edge targets must be real tag names | live (J-11) |
| REQ-12 / J-05 | Owner follows then browses public lanes | Public discovery not rewritten by edges | Load-bearing non-goal: no personalization this INIT | live (J-05) |
| REQ-13 / J-13 | Dissolve then re-establish same name | Edge returns once | Continuity of edge lifecycle beyond one-shot CRUD | live (J-13) |
| REQ-14 / J-14 | Owner has author subscriptions + tag edges | Subscription stream unchanged by tag edges | Noun / graph separation from INIT-002 | live (J-14) |
| REQ-15 / J-15 | Owner has parked searches + tag edges | Objects stay separate | Noun / surface separation from INIT-003 | live (J-15) |
| REQ-16 / J-16 | Owner follows; peer/guest browses that lane | Public lane stays ungated and unpersonalized for others | Private edge is not a lane ACL | live (J-16) |
| REQ-17 / J-17 | Two members follow same tag; one unfollows | Only the actor’s edge dissolves | Directed edges are membership-scoped, not shared | live (J-17) |
| REQ-18 / J-18 | Actor seeks inbound followers-of-tag | No disclosure this INIT | Anti-reciprocity — kills social-harvest side door | live (J-18) |
| REQ-19 / J-02 | Follow tag with empty public lane | Edge allowed; list shows name | Corpus emptiness must not block private edge establish | live (J-02) |
| REQ-20 / J-01 | Re-follow already-edged name | Still one edge; no required conflict | Idempotent stewardship without duplicate rows | unit / live (J-01) |
| REQ-22 | Tag name with outer whitespace | Trimmed identity; case-sensitive after trim | Prevents duplicate edges from whitespace-only variance | unit / live (J-01, J-11) |

## Out of scope for this repo

- Settings (or any) web UI for tag-follow edge stewardship — **realworld-web** (deferred per impact map)
- Local compose / env delta for API-only live prove hosting — **realworld-local** (deferred; optional host does not mint a CAP)
- Feed personalization / ranking / “articles matching my followed tags” as a required success path
- Public who-follows-this-tag social proof (counts, actor lists, reverse-index queries)
- Treating tag-follow as author-follow, or composing silent “author-subscription ∩ tag-follow” discovery
- Reopening INIT-REALWORLD-001 publish / seat / favorites / nameplate / public tag-lane requirement sets
- Reopening INIT-REALWORLD-002 author subscription / subscription-stream rules
- Reopening INIT-REALWORLD-003 parked search memory rules
- Viewer-relative “following” CTA state on public tag surfaces this INIT (IM-07 / OQ-07 deferred)
- Owner-visible history of former tag follows after dissolve (IM-08 / OQ-08 deferred)
- Comments, OAuth, email verification, mobile/native clients
- Admin/moderation tooling over other members’ tag-follow edges
- Cross-member transfer or export programmes
- New infra services beyond the existing catalog
- C1 topic-watchlist, C2 interest-signal ledger, or C3 lane-bookmark packaging as primary product nouns

## Cross-service contracts

None — no cross-repository boundary. Stewardship is owned and proven on `realworld-api`; `realworld-web` settings UI is an explicit non-goal; `realworld-meta` carries product truth only (PRD §8; impact-map §6).

## Non-functional requirements

| Area | Requirement or N/A rationale | Acceptance / evidence |
|------|------------------------------|-----------------------|
| Security | Seat-bound stewardship; unseated and peer access fail closed (REQ-02, REQ-07–REQ-10). No inbound who-follows-tag surface (REQ-18). Edges are not lane ACLs (REQ-16). Missing/non-owned dissolve is indistinguishable not-found (REQ-10). | unit + live denial / isolation paths |
| Reliability | N/A beyond fail-closed follow/list/unfollow behavior — not a multi-region SLA INIT. Incomplete establish must not leave a visible edge that disagrees with refusal rules. | inspection / negative-path tests |
| Performance / capacity | N/A for guinea-pig scale; no concurrent-load target locked. Per-member outgoing-edge count and max tag-name length may use eng reasonableness limits (IM-04) without inventing product caps this INIT. | N/A |
| Observability | N/A as product REQ — operational logging remains an engineering concern (chassis rules). | N/A for product acceptance |
| Privacy / data handling | Outgoing tag-follow edges are private to the owning membership; peers and guests must not observe the set (REQ-07, REQ-09) or reverse-index it (REQ-18). | live (J-06, J-07, J-18) |
| Migration / compatibility | Additive private state for existing members; default empty own outgoing set. Does not migrate or rewrite INIT-001 favorites, INIT-002 author-follow edges, or INIT-003 parks. Does not rewrite public lane membership this INIT. Distinct from legacy author-follow tables under `app/`. | as-built / feasibility |
| Rollback / recovery | N/A as product REQ — delivery rollback is engineering. | N/A |
| Operations / support | No new infra services; prove against existing `realworld-api` (local compose may host prove without expanding product scope to web UI). | N/A in-repo |

## Assumptions

| ID | Assumption | Evidence | Owner | Status | Invalidated when |
|----|------------|----------|-------|--------|------------------|
| A-01 | INIT-REALWORLD-001 contribution-seat semantics (login seats, logout unseats) remain the gate for “signed-in reader” | PRD A-01; sibling spec `INIT-REALWORLD-001-api.md` | PM | confirmed | Lead reopens seat meaning conflicting with this INIT |
| A-02 | Tag-follow is a distinct product object from INIT-002 author subscription; “follow” in this INIT means membership→tag edge only | PRD A-02; REQ-01–REQ-22 | PM | confirmed | Lead intended author-follow reuse — kill noun and reopen |
| A-03 | Durable retention means membership-scoped persistence across logout/login, not merely in-process memory | PRD A-03; REQ-05 | PM | confirmed | Lead wants session-only memory |
| A-04 | Two distinct gates apply: (a) unseated fail-closed for follow/list/unfollow, and (b) peer / inbound opacity so seated peers cannot observe or reverse-index another member’s outgoing edges | PRD A-04; REQ-02, REQ-07–REQ-09, REQ-18 | PM | confirmed | Lead allows peer visibility or inbound follower lists |
| A-05 | Owner list exposing tag names is sufficient edge-fidelity proof without web UI or personalized feed this INIT | PRD A-05; impact-map deferred web | PM | confirmed | Lead makes UI or feed personalization a kill path |
| A-06 | Public tag-lane / bulletin discovery and INIT-002 subscription-stream rules remain baseline and are not rewritten by this INIT’s edges | PRD A-06; REQ-12, REQ-14, REQ-16 | PM | confirmed | Edges must alter lane or stream membership — different INIT |
| A-07 | Membership→tag follow edge is a different product object from INIT-003 parked search memory | PRD A-07; REQ-15 | PM | confirmed | Lead intended search-park reuse — kill noun and reopen |
| A-08 | “Follow edge” this INIT means durable directed ownership-bound relationship continuity, not a bidirectional social graph or public follower index | PRD A-08; REQ-07, REQ-17, REQ-18 | PM | confirmed | Inbound social proof required for kill |
| A-09 | Concurrent same-tag follows by different members are independent edges, not a shared multiset row | PRD A-09; REQ-17 | PM | confirmed | Shared edges intended — ownership REQs need redesign |
| A-10 | As-built index is absent; source under `app/` has author-follow (`profiles` follow routes) and public tag catalog, but **no** membership→tag follow-edge tables or stewardship routes — CAP-01..CAP-03 are new prove surfaces | Source scan 2026-11-12; missing `docs/specification/as-built/` | PE | open | As-built index published with capability rows |

## Spec questions (ambiguities — need PM or domain confirmation before feasibility)

| ID | Lane | Question | Owner | Blocking | Required by | Default if deferred | Status | Resolution link |
|----|------|----------|-------|----------|-------------|---------------------|--------|-----------------|
| Q-01 | PM | May a seated member establish an edge to a tag name with zero current articles? (OQ-01 / IM-01) | PM | no | feasibility | Allow any non-empty normalized tag name even if no article currently carries it | resolved | Impact-Map IM-01 default → REQ-19 |
| Q-02 | PM | Is re-follow of an already-edged tag name idempotent success or a distinct conflict? (OQ-02 / IM-02) | PM | no | feasibility | Idempotent success — list still shows the tag once | resolved | Impact-Map IM-02 default → REQ-20 |
| Q-03 | PM | Exact fail-closed shape for unfollow when not following vs non-owned / missing identity (OQ-03 / IM-03) | PM | no | feasibility | Indistinguishable not-found; no outgoing-edge contents disclosed | resolved | Impact-Map IM-03 default → REQ-10 |
| Q-04 | PM | Per-member max outgoing edges and max tag-name length (OQ-04 / IM-04) | PM | no | feasibility | Eng reasonableness limits acceptable | resolved | Impact-Map IM-04 default → NFR Performance |
| Q-05 | PM | Owner outgoing-list ordering rule (OQ-05 / IM-05) | PM | no | feasibility | Newest-established-first; timestamp source eng | resolved | Impact-Map IM-05 default → REQ-21 |
| Q-06 | PM | Tag-name normalization for identity equality (OQ-06 / IM-06) | PM | no | feasibility | Trim outer whitespace; case-sensitive after trim | resolved | Impact-Map IM-06 default → REQ-22 |
| Q-07 | PM | Must establish appear as viewer-relative “following” state on public tag surfaces? (OQ-07 / IM-07) | PM | no | later | No — private outgoing-edge surface is enough this INIT | open | Impact-Map IM-07; Out of scope |
| Q-08 | PM | Does dissolve leave owner-visible history of former tag follows? (OQ-08 / IM-08) | PM | no | later | Fully removed from owner outgoing list — no history surface | open | Impact-Map IM-08; Out of scope |
| Q-09 | PM | Must favorites and tag-follow edges stay mutually invisible beyond non-reopen? (OQ-09 / IM-09) | PM | no | later | Yes — separate surfaces; no cross-write this INIT | open | Impact-Map IM-09; aligns with REQ-15 pattern / Out of scope cross-write |
| Q-10 | PM | May any future programme reverse-index tag-follow edges without a new INIT? (OQ-10 / IM-10) | PM | no | later | No — inbound disclosure requires a later INIT | open | Impact-Map IM-10; REQ-18 stands |
| Q-11 | PE | How to introduce membership→tag follow-edge persistence and stewardship routes on the legacy Conduit `app/` baseline (distinct from author-follow `profiles` routes) vs platform `src/` chassis for CAP-01..CAP-03 | PE | no | technical review | Satisfy REQs on Accepted ADR-001 Option A (`app/`) unless TDD supersedes; do not reuse author-follow tables as the tag-edge store | open | Feasibility / technical review |

## Draft check summary (D1–D12)

| Check | Status | Evidence / findings |
|-------|--------|---------------------|
| D1 Approved handoff current | PASS | H1 digest matches PRD file `sha256:93c847c6…`; H3 map_revision=1; H2 api scope digest `sha256:383c6d92…`; G1 APPROVED review `commit_id` = meta PR #12 head `02c74d94…`; label `impact-map-lgtm`; repo affected not deferred/blocked |
| D1b No open blocking IM-* | PASS | Impact-map §10: IM-01..IM-10 all `Blocking: no`; Gate 1 note allows defaults for spec-draft |
| D2 Complete PRD traceability | PASS | CAP-01..CAP-03 each have ≥1 REQ; every REQ cites PRD CAP/REQ or OQ/IM default |
| D2b Journeys carried | PASS | J-01..J-18 carried; live evidence cites CAP/J |
| D3 Repo-bounded scope | PASS | Provider scope matches impact-map H2; web/local deferred and non-goals listed under Out of scope |
| D4 Observable acceptance | PASS | Each REQ has condition/event, observable result, evidence layer; implementation-neutral |
| D5 Negative/failure paths | PASS | Table covers empty/blank, unseated, peer isolation, empty list, missing identity, durability, non-composition, anti-reciprocity, idempotency |
| D6 Assumptions/questions | PASS | Assumptions evidenced; questions have lane/owner/blocking/default/status; material PM defaults applied into REQs |
| D7 Cross-repository contracts | PASS | None — no cross-repo product seam (PRD §8; impact-map §6) |
| D8 NFR applicability | PASS | All eight areas specified or N/A with reason |
| D9 As-built alignment | PASS | As-built index absent; source scan: author-follow + public tags exist; no membership→tag follow-edge surface — CAP-01..CAP-03 are new; seat/auth baseline from INIT-001 remains |
| D10 Dependency order | PASS | Matches impact-map: sole build order `drivestream-lab/realworld-api`; api depends on none |
| D11 Zero unresolved blockers | PASS | No blocking Q remaining; Q-07..Q-11 non-blocking with defaults / later revisit |
| D12 Output completeness | PASS | Header H1–H3/G1, tables, check summary, outcome, PR readiness, handoff present |

**Draft verdict:** PASS

**Selected workflow outcome:** `pass`
**Outcome reason:** D1–D12 PASS, Gate 1 current, zero unresolved material questions, IM defaults locked into REQs, PR READY for Forge publish.

Do not advance to `/initiative-feasibility` unless the workflow outcome is
`pass`, the draft verdict is PASS, and the developer review below is complete.

## PR readiness handoff

| Item | Value |
|------|-------|
| Workflow outcome | `pass` — D1–D12 PASS; Gate 1 current; material IM defaults applied |
| Verdict | PR READY |
| Existing spec PR | none |
| Proposed branch | `chore/INIT-REALWORLD-004-spec-realworld-api` |
| Proposed base | `develop` |
| Proposed title | `[INIT-REALWORLD-004] Spec — realworld-api` |
| PR type | **Draft** (entire spec lifecycle) |
| Local artifacts to publish | `docs/specification/product/INIT-REALWORLD-004-api.md`, `docs/specification/README.md` |
| Forge readiness | fill `handoff.forge` for `open_draft_pr`; recommend `/commit-workspace` then `/open-draft-pr` — do not commit/push/open PR inside this skill |
| Reviewer | @drivestream-lab/backend-devs |
| Initial Gate 2 label | `spec-pending` |
| Additional invalidation label | none |
| Blocking items | none |

**No GitHub side effects have occurred.** Persist the draft locally; Forge publish is a later `/commit-workspace` / `/open-draft-pr` or Gateflow ForgeClient step.

### Proposed Draft PR body

```markdown
## Initiative

INIT-REALWORLD-004 — Private membership→tag follow edges

## Meta handoff

- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/12
- Approved meta head: `02c74d94cf8748c1cd53a268035a8a84433caf94`
- Impact-map revision: 1
- PRD digest: `sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3`
- Repo scope digest: `sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5`

## Spec path

`docs/specification/product/INIT-REALWORLD-004-api.md`

## Summary

- 22 REQs covering CAP-01..CAP-03 as API provider (no cross-repo CTR this INIT)
- Establish / list / dissolve membership→tag follow edges with durability, peer/unseated isolation, anti-reciprocity, and non-composition; web/local out of scope
- Open non-blocking questions: Q-07..Q-11 (later / PE chassis)

## Gate 2 — spec package readiness

Initial label: `spec-pending`

- [ ] Spec slice published on this PR head (via Forge `/commit-workspace` / `/open-draft-pr`)
- [ ] Feasibility report (later Forge publish)
- [ ] Technical design + ADRs (later Forge publish)
- [ ] Implementation plan §9 (later Forge publish)
- [ ] PE sets `spec-lgtm` on exact final head before merge

Requested reviewer: @drivestream-lab/backend-devs
```

## Developer review

- [ ] Scope matches the approved impact-map repo scope digest
- [ ] REQs have condition/event, observable result, and evidence layer
- [ ] Contracts are semantic (logical operation); no architecture decisions in REQs
- [ ] No blocking question remains
- [ ] Developer confirmed draft is ready for feasibility

## After Draft PR creation

PE controls Gate 2 labels on the spec PR. Never infer approval from labels
alone — `spec-lgtm` requires matching artifacts on the exact PR head.

Provision labels before PR creation when missing:

```bash
launchpad apply-gates --repo realworld-api --apply
```

| PE action | Remove | Add |
|-----------|--------|-----|
| Pending/new revision | `spec-lgtm`, `spec-blocked` | `spec-pending` |
| Request changes/hold | `spec-pending`, `spec-lgtm` | `spec-blocked` |
| Approve full package | `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale` | `spec-lgtm` |

## References

- PRD: `realworld-meta/prd/INIT-REALWORLD-004.md`
- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/12
- Spec PR: pending
- Service profile: not present (`docs/specification/product/00-service-profile.md` absent)

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-draft
  outcome: pass
  artifact:
    path: docs/specification/product/INIT-REALWORLD-004-api.md
  blockers: []
  signals:
    pr_ready: true
    draft_verdict: PASS
    map_revision: 1
    meta_pr: https://github.com/drivestream-lab/realworld-meta/pull/12
    meta_pr_approved_head: 02c74d94cf8748c1cd53a268035a8a84433caf94
    prd_digest: sha256:93c847c6e063476413c9ca37e8f76ae2d709a425d9d908b57666a0797b037ff3
    scope_digest: sha256:383c6d9230804e3cfe4007373df6cf732d6a9415eb5725e1a7c13bfb3e78b0f5
    open_non_blocking_questions:
      - Q-07
      - Q-08
      - Q-09
      - Q-10
      - Q-11
  next_candidates:
    - spec-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-004] Spec — realworld-api"
    body_path: docs/specification/product/INIT-REALWORLD-004-api.md
```
