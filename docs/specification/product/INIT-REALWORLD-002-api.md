# INIT-REALWORLD-002 — spec slice for realworld-api

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-002 |
| PRD | `realworld-meta/prd/INIT-REALWORLD-002.md` |
| PRD digest (H1) | `sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92` |
| Meta PR | https://github.com/drivestream-lab/realworld-meta/pull/8 |
| Meta PR approved head (G1) | `ee9fe45ad23d988eface7517a3a65a7b58b592c1` |
| Impact map | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-002.md` |
| Impact-map revision (H3) | `1` |
| Repo scope digest (H2) | `sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0` |
| Tech-lead approval | Review `PRR_kwDOVac9Rs8AAAABXAtAcQ` / id `5839208561` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T08:58:03Z`; `commit_id` = `ee9fe45ad23d988eface7517a3a65a7b58b592c1` (matches merged meta PR #8 head; label `impact-map-lgtm`) |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Status | Draft — dev review required before Forge publish |

> **H4 citations:** The H1–H3 (and G1) rows above are the durable authority
> carrier for mid-lane freshness. Feas / TDD / plan digests are walk-time only
> and may be purged at initiative closure — see
> `prayog-skills/references/artifact-write-contract.md`.

## Overview

`realworld-api` is the **provider** for CAP-01..CAP-04 and CTR-01..CTR-04: ungated unpersonalized public discovery; seat-bound author subscribe/unsubscribe with viewer-relative subscription state and persistence across unseat/reseat; denial-honest empties and fail-closed unseated/self/missing-author outcomes; subscription-stream lifecycle honesty including publish-in, delete-out, empty-stream validity, and stream privacy.

**Out of this repo:** Guest/member UAT chrome and kill-path driving (`realworld-web`); local compose prove environment (`realworld-local`); follower/following **counts** as social proof (OQ-01 / IM-01 deferred); comments; OAuth; email verification; mobile/native clients; reopening INIT-REALWORLD-001 favorites/nameplate rules; composed subscription∩tag discovery; mutual-friends packaging.

**Ownership:** this spec states observable API product behavior, acceptance, field meaning, invariants, errors, and compatibility only. Implementation architecture (chassis under `app/` vs `src/`, persistence, transport encoding) is **not** decided here — routed to feasibility / technical review.

**Baseline:** INIT-REALWORLD-001 seat/bulletin rules remain in force and are not reopened. This INIT adds author-subscription and subscription-stream trust on top of that seat. REQ-01–REQ-06 re-prove ungated public discovery and subscription-independent listing continuity; they do not re-own INIT-001 requirement ids.

## Functional requirements

| ID | Requirement | PRD source | Condition / event | Observable result | Evidence layer |
|----|-------------|-----------|-------------------|-------------------|----------------|
| REQ-01 | Expose the public article listing without requiring a contribution seat | PRD REQ-01 / CAP-01 | Guest (no authenticated seat) requests the public article listing | Listing state returned (populated or empty); no account wall / auth challenge required for this read | live (CAP-01, J-01) |
| REQ-02 | Expose a single published article without a contribution seat | PRD REQ-02 / CAP-01 | Guest requests a published article that exists | Published content returned while still unseated | live (CAP-01, J-01) |
| REQ-03 | Expose public tag surfaces without a contribution seat | PRD REQ-03 / CAP-01; IM-04 / OQ-04 default | Guest requests the tag catalog or a tag lane (including unknown/blank-normalized tags) | Tag surface usable without auth; unknown/blank-normalized tags yield an empty lane (not unrelated articles) | live (CAP-01, J-02) |
| REQ-04 | Keep public discovery reads available when a subscribe affordance is present on public author/article surfaces | PRD REQ-04 / CAP-01 | Guest requests public listing, published open, or tag surfaces on a surface that also exposes subscribe to seated actors | Public discovery completes without requiring authentication | live (CAP-01, J-09) |
| REQ-05 | Keep public discovery membership independent of the viewer’s subscriptions | PRD REQ-05 / CAP-01 | Seated member subscribes or unsubscribes, then re-requests public listing and a tag lane | Public listing and tag-lane memberships do not add/remove articles solely because subscriptions changed | live (CAP-01, CAP-04, J-14) |
| REQ-06 | Keep the seated global article listing subscription-independent | PRD REQ-06 / CAP-01 | Seated member requests the global article listing when published articles exist | Membership agrees with the global-feed contract and does not depend on the viewer’s subscriptions | live (CAP-01, J-03) |
| REQ-07 | Subscribe to another author and report viewer-relative subscription state true | PRD REQ-07 / CAP-02; IM-01 / OQ-01 default | Seated member subscribes to an author they do not already subscribe to | Viewer-relative subscription boolean for that author becomes subscribed; subsequent seated reads agree; no follower/following **counts** required | live (CAP-02, J-04) |
| REQ-08 | Unsubscribe from an author and report viewer-relative subscription state false | PRD REQ-08 / CAP-02; IM-01 / OQ-01 default | Seated member unsubscribes from an author they currently subscribe to | Viewer-relative subscription boolean becomes not-subscribed; subsequent seated reads agree; no counts required | live (CAP-02, J-04) |
| REQ-09 | Persist subscription edges across unseat and reseat | PRD REQ-09 / CAP-02 | Seated member subscribes to an author, logs out, then logs in again without changing edges while unseated | After reseat, viewer-relative subscription state for that author is still subscribed | live (CAP-02, J-13) |
| REQ-10 | Refuse self-subscribe | PRD REQ-10 / CAP-03; IM-09 / OQ-09 default | Seated member attempts to subscribe to their own author identity | Subscription graph unchanged; subscription state toward self does not become subscribed | unit / live (CAP-03, J-07) |
| REQ-11 | Deny subscribe and unsubscribe while unseated | PRD REQ-11 / CAP-03 | Guest or post-logout actor attempts subscribe or unsubscribe | No subscription-edge change; fail closed | live (CAP-03, J-10) |
| REQ-12 | Refuse subscribe of a missing or unknown author identity | PRD REQ-12 / CAP-03; IM-03 / OQ-03 default | Seated member attempts to subscribe to an author identity that does not exist (or is deactivated per product meaning) | Subscription graph unchanged; fail closed | unit / live (CAP-03, J-12) |
| REQ-13 | Allow an empty subscription stream as a valid outcome | PRD REQ-13 / CAP-03 | Seated member with zero subscriptions (or subscribed authors with zero published articles) requests the subscription stream | Empty stream returned; must not silently equal global public membership; must not present as an auth or hard-error wall | live (CAP-03, CAP-04, J-08) |
| REQ-14 | Keep guest public discovery working after a member unseats | PRD REQ-14 / CAP-03 | Member who previously used subscriptions logs out, then requests public articles/tags as Guest | Public discovery still works without auth friction; subscription mutations remain denied | live (CAP-01, CAP-03, J-10) |
| REQ-15 | Present the subscription stream for the seated member | PRD REQ-15 / CAP-04 | Seated member who subscribes to at least one author that has published articles requests the subscription stream | Stream contains only published articles authored by authors that member currently subscribes to | live (CAP-04, J-05) |
| REQ-16 | Remove an author’s articles from the subscription stream after unsubscribe | PRD REQ-16 / CAP-04 | Seated member unsubscribes from an author who had articles in that stream | Those articles no longer appear in the subscription stream; public/global membership is unchanged by unsubscribe alone | live (CAP-04, J-06) |
| REQ-17 | Include a subscribed author’s newly published article in the subscription stream | PRD REQ-17 / CAP-04 | Seated member already subscribes to an author; that author then publishes a new tagged article; subscriber re-requests the stream | The new article appears in the subscriber’s subscription stream; public listing/tag membership update as public-discovery rules require without depending on who subscribes to whom | live (CAP-04, J-11) |
| REQ-18 | Remove a deleted article from the subscription stream | PRD REQ-18 / CAP-04; IM-11 / OQ-11 default | Seated member subscribes to an author; that author deletes a published article that was in the subscriber’s stream; subscriber opens the stream again | That article no longer appears in the subscription stream; Guest open-by-reference stays not-found per INIT-001 delete rules | live (CAP-04, J-16) |
| REQ-19 | Keep the subscription stream private to the subscriber | PRD REQ-19 / CAP-04 | Guest (or a peer who is not that subscriber) attempts to obtain another member’s subscription stream membership as a public discovery surface | Other actors do not obtain that member’s stream membership as public truth; Guest public discovery remains the ungated surface | live (CAP-04, CAP-01, J-15) |
| REQ-20 | Keep tag-lane membership tag-true under subscription churn | PRD REQ-20 / CAP-04; IM-08 / OQ-08 default | Member subscribes or unsubscribes without changing article tags | Tag lanes still reflect tag membership only — not subscription state; no composed subscription∩tag listing surface | live (CAP-04, CAP-01, J-14) |
| REQ-21 | Order global listing and subscription stream newest-first by the same publish/update time rule | PRD OQ-02 / IM-02 default; CAP-01 / CAP-04 | Seated member (or Guest for global) requests global listing or subscription stream with ≥2 eligible articles | Listing order is newest-first by the article’s publish/update time (same rule family as INIT-001 OQ-06 default); exact timestamp source left to engineering | integration / live (CAP-01, CAP-04, J-03, J-05) |
| REQ-22 | Omit seated-only subscription state for Guest profile reads | PRD OQ-05 / IM-05 default; CAP-02 / CAP-03 | Guest requests a public author presentation | Seated-only viewer-relative subscription state is omitted (not presented as another member’s edges); public discovery remains ungated; subscribe affordance may be advertised without gating reads | live (CAP-01, CAP-02, J-09) |
| REQ-23 | Leave already-subscribed subscribe attempts as subscribed without requiring a distinct error | PRD OQ-10 / IM-10 default; CAP-02 | Seated member who already subscribes to an author attempts subscribe again | Viewer-relative state remains subscribed; graph unchanged; distinct error not required | unit / live (CAP-02, J-04) |

> **Id convention:** `REQ-*` is canonical (`prayog-skills/references/id-conventions.md`).
> Legacy display alias `FR-{nn}` ≡ `REQ-{nn}` — prefer `REQ-*`.
>
> **Behavioral acceptance vs evidence:** Condition/event + observable result are
> the product acceptance statement (implementation-neutral). Evidence layer
> names how it will be proved later. Live evidence cites `CAP-*` and/or `J-*`.

## Capabilities (carried from PRD)

| ID | Capability | Journeys | Notes |
|----|------------|----------|-------|
| CAP-01 | Ungated unpersonalized public discovery | J-01, J-02, J-03, J-09, J-10, J-14 | Provider of CTR-01 / CTR-04; never requires a seat; membership independent of subscriptions |
| CAP-02 | Seat-bound author-subscription stewardship | J-04, J-06, J-07, J-10, J-12, J-13 | Provider of CTR-02; viewer-relative boolean only (IM-01); persistence across reseat |
| CAP-03 | Denial-honest empties and fail-closed outcomes | J-07, J-08, J-10, J-12, J-15 | Empty stream/listing/lane valid; unseated/self/missing denials fail closed; no silent global-fill |
| CAP-04 | Subscription-stream lifecycle honesty | J-05, J-06, J-08, J-11, J-14, J-15, J-16 | Provider of CTR-03; stream ⊆ subscribed authors’ published articles; publish-in / delete-out; private to subscriber |

## Journeys (carried from PRD)

| ID | Actor | Trigger | Main flow | Primary edge | Abandon | Caps |
|----|-------|---------|-----------|--------------|---------|------|
| J-01 | Guest | Wants public articles without signing in | Opens public listing → opens a published article when present → reads | Empty listing → still ungated | Leaves without registering | CAP-01 |
| J-02 | Guest | Explores topics | Opens tag catalog/lane → scans → opens a matching article when present | Empty lane for that tag only | Leaves tags | CAP-01 |
| J-03 | Seated member | Checks unpersonalized global listing | Opens global article listing → confirms membership is not subscription-filtered | Empty global listing still readable | Leaves listing | CAP-01 |
| J-04 | Seated member | Builds / clears a subscription | Opens an author’s public presentation → subscribes → sees state true → unsubscribes → sees false | Self-subscribe attempt → refused (J-07) | Cancels without subscribe | CAP-02 |
| J-05 | Seated member | Uses the subscription stream | Subscribes to an author who has published articles → opens subscription stream → opens one such article | If author has no articles → empty stream (J-08) | Unsubscribes (J-06) | CAP-04 |
| J-06 | Seated member | Proves stream honesty after unsubscribe | Unsubscribes → state false → stream loses that author’s articles → global listing unchanged by unsubscribe alone | Last unsubscribe → empty stream | N/A — unsubscribe is the act | CAP-04, CAP-02 |
| J-07 | Seated member | Attempts self-subscribe | Tries to subscribe to own author identity | Graph unchanged; denial observed | Returns to other authors | CAP-03, CAP-02 |
| J-08 | Seated member | Opens stream with nothing to show | Subscribes to zero authors (or subscribed authors silent) → opens subscription stream | Empty state; must not silently show global membership; not an error wall | Switches to global listing | CAP-03, CAP-04 |
| J-09 | Guest | Sees subscribe affordance while browsing | Views public author/article surface that offers subscribe to seated actors → continues public discovery without authenticating | If Guest tries subscribe → denied (J-10) | Leaves | CAP-01 |
| J-10 | Seated → Guest | Unseats after using subscriptions | Subscribes → logs out → completes public listing/open as Guest → attempts subscribe/unsubscribe | Public discovery works; mutations fail closed | Reseats (J-13) | CAP-01, CAP-03, CAP-02 |
| J-11 | Author + Subscriber | Subscribed author publishes | Subscriber already subscribes → Author publishes new tagged article → Subscriber opens subscription stream | New article in stream; public/tag update as ungated discovery | Subscriber unsubscribes first | CAP-04 |
| J-12 | Seated member | Targets a missing author | Attempts subscribe on unknown author identity | Fail closed; graph unchanged (IM-03) | Returns to known authors | CAP-03 |
| J-13 | Seated member | Proves subscription persistence across reseat | Subscribes → logs out → logs in → checks subscription state (and stream if author has articles) | State still subscribed; mutations denied while unseated | Abandons reseat | CAP-02 |
| J-14 | Seated member | Proves public/tag stay unpersonalized under churn | Subscribes/unsubscribes while checking public listing, global listing, and a tag lane | Memberships unchanged by subscriptions alone | Stops probing | CAP-01, CAP-04 |
| J-15 | Guest + Peer | Prove stream privacy | Guest (and/or a peer who is not the subscriber) attempts to treat Member A’s subscription stream as public discovery | A’s stream membership is not revealed as public truth; Guest stays on ungated public discovery | Stops probing | CAP-04, CAP-03 |
| J-16 | Author + Subscriber | Subscribed author deletes | Subscriber already has Author’s article in stream → Author deletes → Subscriber opens subscription stream | Article gone from stream; Guest open-by-reference not-found | Subscriber unsubscribes first | CAP-04 |

## Negative and failure paths

| REQ | Condition | Required behavior | Why it matters | Evidence |
|-----|-----------|-------------------|----------------|----------|
| REQ-01 / REQ-03 | Empty bulletin / empty tag catalog or unknown tag | Empty states still ungated; unknown tag → empty lane | Frictionless ≠ “must have content”; no unrelated fill | live (J-01, J-02) |
| REQ-04 / REQ-22 | Subscribe CTA / profile visible to Guest | Public discovery still ungated; seated subscription state omitted for Guest | Prevents soft auth walls and false edge disclosure | live (J-09) |
| REQ-05 / REQ-06 / REQ-20 | Subscription graph changes | Public/global/tag memberships do not silently become subscription-filtered; no ∩ surface | Unpersonalized discovery kill path | live (J-14) |
| REQ-13 | Subscribing nobody / subscribed authors silent | Empty stream; not an error wall; not silently filled from global | Denial-honest empty kill path | live (J-08) |
| REQ-16 / REQ-08 | After unsubscribe | Stream loses articles; subscription state false; global untouched by unsubscribe alone | Stream honesty | live (J-06) |
| REQ-10 | Self-subscribe attempt | Fail closed; graph unchanged | Graph integrity | unit / live (J-07) |
| REQ-11 / REQ-14 | Unseated subscribe cluster | Fail closed; guest public discovery remains open | Seat boundary + kill path | live (J-10) |
| REQ-12 | Subscribe missing/unknown author | Fail closed; graph unchanged | No ghost edges | unit / live (J-12) |
| REQ-09 | Logout then login | Subscriptions still present after reseat; mutations still denied while unseated | Persistence ≠ keep seat | live (J-13) |
| REQ-17 | Subscribed author publishes | Stream gains article on re-open; public/tag update as discovery | Lifecycle honesty | live (J-11) |
| REQ-18 | Subscribed author deletes | Stream loses article on next open; no ghost readable body via stream | Lifecycle honesty + INIT-001 delete coherence | live (J-16) |
| REQ-19 | Guest/peer probing another’s stream | No public reveal of that stream membership | Stream privacy | live (J-15) |
| REQ-23 | Already-subscribed subscribe | Remains subscribed; no required distinct error | Idempotent stewardship without false denials | unit / live (J-04) |

## Out of scope for this repo

- Guest/member UAT chrome, client navigation, and kill-path driving — **realworld-web**
- Local compose / DB join for live prove — **realworld-local**
- Follower/following **counts** as social proof (OQ-01 / IM-01 deferred — boolean only)
- Comments (legacy routes may exist in source; not a CAP/REQ of this INIT)
- OAuth / third-party identity; email verification gates
- Mobile or native clients
- Reopening INIT-REALWORLD-001 publish / seat / favorites / nameplate requirement sets
- Public who-favorited social proof
- Composed “subscription ∩ tag” discovery surface (IM-08)
- Mutual-follow ceremony or “friends” packaging beyond directed subscriptions
- Mid-view push without re-open for last-unsubscribe empty chrome (OQ-06 / IM-06) or same-visit delete-out without re-open (OQ-11 / IM-11) — next open / re-check sufficient
- Clarification-budget / Buzz / OKF ceremony as product CAP/REQ (programme vehicle only)

## Cross-service contracts

| Contract ID | Provider / owner | Consumer / owner | Entry point | Input shape | Output shape | Invariants | Errors | Compatibility / versioning | Contract-test location |
|-------------|------------------|------------------|-------------|-------------|--------------|------------|--------|----------------------------|------------------------|
| CTR-01 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Read ungated unpersonalized public discovery | Identity of listing mode (global / tag / author), article reference, public author presentation | Global listing, tag-filtered listing, single published article, public author presentation; empty sets allowed | Reading never requires a seat; only published articles appear; empty listing/lane allowed; membership does not depend on viewer subscriptions; newest-first ordering (REQ-21) | Missing article → stable not-found; empty sets allowed | New INIT-002 seam on INIT-001 bulletin baseline; breaking change requires INIT revision | planned under `tests/verify` / consumer contract suite (TBD in plan) |
| CTR-02 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Manage author subscriptions and report viewer-relative state | Subscribe / unsubscribe target author identity; seated session; seated profile read for state | Viewer-relative subscription boolean (true/false); mutation confirmation; Guest profile reads omit seated-only state (REQ-22) | Seat required to mutate; self-subscribe refused; missing author refused; directed edges; state matches edge; edges persist across unseat/reseat; unseated mutate denied; counts out of scope (IM-01); already-subscribed subscribe may leave state subscribed (REQ-23) | Unauthenticated; self target; missing author | New INIT-002 seam | planned under `tests/verify` (TBD in plan) |
| CTR-03 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Read subscription stream | Seated session; optional pagination identity | Seated-only listing of published articles by currently subscribed authors; empty stream allowed | Stream ⊆ articles authored by currently subscribed authors; empty stream allowed; must not silently equal global membership when subscriptions are empty; stream is not a public discovery surface for other actors; newest-first (REQ-21); publish-in / delete-out on re-open | Unauthenticated; empty sets allowed | New INIT-002 seam | planned under `tests/verify` (TBD in plan) |
| CTR-04 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Keep tag-true discovery under subscription churn | Tag catalog identity; per-tag lane identity | Tag catalog and per-tag article membership | Lane membership reflects current tags only; independent of subscriptions; empty lane allowed (including unknown/blank-normalized tags per IM-04); no silent subscription∩tag composition | Unknown tag → empty lane | New INIT-002 seam | planned under `tests/verify` (TBD in plan) |

## Non-functional requirements

| Area | Requirement or N/A rationale | Acceptance / evidence |
|------|------------------------------|-----------------------|
| Security | Subscribe/unsubscribe fail closed while unseated (REQ-11). Self-subscribe refused (REQ-10). Guest public discovery must not be gated by auth (REQ-01–REQ-04, REQ-14). Missing-author subscribe refused (REQ-12). Subscription stream not a public reveal surface (REQ-19). Guest must not receive another viewer’s seated subscription edges as truth (REQ-22). | unit + live denial / privacy paths |
| Reliability | N/A beyond fail-closed trust behavior — not a multi-region SLA INIT. Incomplete subscribe/unsubscribe must not leave partial edge success that disagrees with reported state. | inspection / negative-path tests |
| Performance / capacity | N/A for this INIT; no concurrent-load target locked. | N/A |
| Observability | N/A as product REQ — operational logging remains an engineering concern (chassis rules). | N/A for product acceptance |
| Privacy / data handling | Viewer-relative subscription boolean is in scope; follower/following **counts** deferred (IM-01). Guest must not be shown another viewer’s seated subscription state or stream as authoritative truth (REQ-19, REQ-22). No who-favorited proof. | live (J-09, J-15) |
| Migration / compatibility | Builds on INIT-REALWORLD-001 clean-slate corpus; subscriptions are additive social state, not a rewrite of INIT-001 favorites. Stream lifecycle must stay coherent with INIT-001 publish/delete. Legacy Conduit-shaped follow/feed code under `app/` is baseline source, not a guaranteed as-built product surface until proven. | as-built / feasibility |
| Rollback / recovery | N/A as product REQ — delivery rollback is engineering. | N/A |
| Operations / support | Live prove environment is `realworld-local` compose (out of this repo); no 24×7 support envelope locked. | N/A in-repo |

## Assumptions

| ID | Assumption | Evidence | Owner | Status | Invalidated when |
|----|------------|----------|-------|--------|------------------|
| A-01 | INIT-REALWORLD-001 seat/bulletin rules stay in force; this INIT does not weaken guest read or seated contribution gates | PRD A-01; sibling spec `INIT-REALWORLD-001-api.md` | PM | confirmed | Lead reopens INIT-001 conflicting REQs |
| A-02 | Named RealWorld programme contracts for global feed, following feed, tags, and follow edges exist as api↔web meaning to pin (upstream Conduit shape); “follow” maps to author subscription here | PRD A-02; CTR-01..CTR-04 | PM | confirmed | A named contract is missing — mint OQ and block seam, do not invent eng payloads |
| A-03 | “Auth friction” means any requirement to authenticate before completing public listing/tag/open | PRD A-03 | PM | confirmed | Soft walls that block public discovery are redefined as acceptable |
| A-04 | Empty subscription stream is valid and must not silently fall back to global membership | PRD A-04; REQ-13 | PM | confirmed | Product later wants silent global fallback (new Lock) |
| A-05 | Viewer-relative subscription boolean is sufficient for “author follow state”; counts are out of scope | PRD A-06; IM-01 default | PM | confirmed | Lead requires counts (resolve OQ-01 into REQs) |
| A-06 | Logout unseats but does not wipe the membership’s subscription graph; reseat restores the same edges | PRD A-07; REQ-09 | PM | confirmed | Lead wants ephemeral subscriptions-per-session |
| A-07 | Subscription-stream publish-in and delete-out are required on re-open; mid-view push without re-open is not required | PRD A-08; IM-06 / IM-11 defaults | PM | confirmed | Lead requires live push without re-check |
| A-08 | As-built index is absent; source under `app/` includes legacy Conduit follow/profile/feed routes that partially resemble CAP-02..CAP-04 | Source scan 2026-11-12; empty `docs/specification/as-built/` | PE | open | As-built index published with capability rows |
| A-09 | Denial-honest empties are a primary trust bar; C3 mode-switch choreography and C2 parity tables are not required as primary CAP framing | PRD A-09 | PM | confirmed | Lead prefers mode/parity nouns as primary cut |

## Spec questions (ambiguities — need PM or domain confirmation before feasibility)

| ID | Lane | Question | Owner | Blocking | Required by | Default if deferred | Status | Resolution link |
|----|------|----------|-------|----------|-------------|---------------------|--------|-----------------|
| Q-01 | PM | Public follower/following counts vs viewer-relative boolean only (OQ-01 / IM-01) | PM | no | feasibility | Boolean subscription state only; counts out of scope | resolved | Impact-Map IM-01 default → REQ-07/REQ-08 / CTR-02 |
| Q-02 | PM | Ordering rule for global listing vs subscription stream (OQ-02 / IM-02) | PM | no | feasibility | Newest-first by same publish/update time rule as INIT-001 OQ-06 default | resolved | Impact-Map IM-02 default → REQ-21 |
| Q-03 | PM | Subscribe/unsubscribe targeting missing or deactivated author (OQ-03 / IM-03) | PM | no | feasibility | Fail closed; graph unchanged | resolved | Impact-Map IM-03 default → REQ-12 |
| Q-04 | PM | Unknown tag: empty lane vs distinct not-found (OQ-04 / IM-04) | PM | no | feasibility | Empty lane for unknown/blank-normalized tags | resolved | Impact-Map IM-04 default → REQ-03 |
| Q-05 | PM | Guest observation of another viewer’s subscription state on public profiles (OQ-05 / IM-05) | PM | no | feasibility | Omit seated-only subscription state for Guest; do not gate public discovery | resolved | Impact-Map IM-05 default → REQ-22 |
| Q-06 | PM | Last-unsubscribe empty-stream chrome without re-open (OQ-06 / IM-06) | PM | no | later | Same visit after re-check/re-open is enough | open | Impact-Map IM-06; API re-open sufficient |
| Q-07 | PM | Clarification rounds counted per CTR vs per product PR thread (OQ-07 / IM-07) | PM | no | later | Per product PR conversation; ≤2 rounds total | open | Programme process only — not an API REQ |
| Q-08 | PM | Composed subscription ∩ tag surface (OQ-08 / IM-08) | PM | no | feasibility | Separate surfaces only; no composed third surface | resolved | Impact-Map IM-08 default → REQ-20 / CTR-04 |
| Q-09 | PM | Own-author self-subscribe affordance chrome (OQ-09 / IM-09) | PM | no | feasibility | No successful self-subscribe path; hide or disable both fine if REQ-10 holds | resolved | Impact-Map IM-09 default → REQ-10 (API refuse); chrome owned by web |
| Q-10 | PM | Already-subscribed subscribe attempt distinguishability (OQ-10 / IM-10) | PM | no | later | Both leave state subscribed; no error required if graph unchanged | resolved | Impact-Map IM-10 default → REQ-23 |
| Q-11 | PM | Subscription-stream delete-out same-visit without re-open (OQ-11 / IM-11) | PM | no | later | Next open of the stream after delete is enough | open | Impact-Map IM-11; API next-open sufficient (REQ-18) |
| Q-12 | PE | How to treat legacy Conduit `app/` follow/feed/profile routes vs Wave chassis under platform `src/` rules for INIT-002 subscription CAPs | PE | no | technical review | Satisfy REQs regardless of chassis; do not expand INIT-002 to comments; architecture chosen in TDD/ADR | open | Feasibility / technical review |

## Draft check summary (D1–D12)

| Check | Status | Evidence / findings |
|-------|--------|---------------------|
| D1 Approved handoff current | PASS | H1 digest matches PRD file `sha256:5a9b49dd…`; H3 map_revision=1; H2 api scope digest `sha256:be0c01c3…`; G1 APPROVED review `commit_id` = meta PR #8 head `ee9fe45a…`; label `impact-map-lgtm`; repo affected not deferred/blocked |
| D1b No open blocking IM-* | PASS | Impact-map §10: no `Blocking: yes` open rows; Gate 1 note allows IM-01..IM-05 and IM-08..IM-09 defaults |
| D2 Complete PRD traceability | PASS | CAP-01..CAP-04 each have ≥1 REQ; every REQ cites PRD CAP/REQ or OQ/IM default |
| D2b Journeys carried | PASS | J-01..J-16 carried; live evidence cites CAP/J |
| D3 Repo-bounded scope | PASS | Provider scope matches impact-map H2; web/local and non-goals listed under Out of scope |
| D4 Observable acceptance | PASS | Each REQ has condition/event, observable result, evidence layer; implementation-neutral |
| D5 Negative/failure paths | PASS | Table covers unseated, self/missing, empty stream, privacy, lifecycle, unpersonalized discovery |
| D6 Assumptions/questions | PASS | Assumptions evidenced; questions have lane/owner/blocking/default/status; material PM defaults applied into REQs |
| D7 Cross-repository contracts | PASS | CTR-01..CTR-04 semantic seams with provider=api, consumer=web |
| D8 NFR applicability | PASS | All eight areas specified or N/A with reason |
| D9 As-built alignment | PASS | As-built index absent; source scan notes legacy Conduit under `app/` (follow/feed/profile present as baseline) vs INIT-002 CAP/REQ obligations (new prove surface); comments present in source but out of scope |
| D10 Dependency order | PASS | Matches impact-map: api → web → local; api depends on none |
| D11 Zero unresolved blockers | PASS | No blocking Q remaining; Q-06/Q-07/Q-11/Q-12 non-blocking with defaults |
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
| Proposed branch | `chore/INIT-REALWORLD-002-spec-realworld-api` |
| Proposed base | `develop` |
| Proposed title | `[INIT-REALWORLD-002] Spec — realworld-api` |
| PR type | **Draft** (entire spec lifecycle) |
| Local artifacts to publish | `docs/specification/product/INIT-REALWORLD-002-api.md`, `docs/specification/README.md` |
| Forge readiness | fill `handoff.forge` for `open_draft_pr`; recommend `/commit-workspace` then `/open-draft-pr` — do not commit/push/open PR inside this skill |
| Reviewer | @drivestream-lab/backend-devs |
| Initial Gate 2 label | `spec-pending` |
| Additional invalidation label | none |
| Blocking items | none |

**No GitHub side effects have occurred.** Persist the draft locally; Forge publish is a later `/commit-workspace` / `/open-draft-pr` or Gateflow ForgeClient step.

### Proposed Draft PR body

```markdown
## Initiative

INIT-REALWORLD-002 — Author-subscription trust with denial-honest empties

## Meta handoff

- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/8
- Approved meta head: `ee9fe45ad23d988eface7517a3a65a7b58b592c1`
- Impact-map revision: 1
- PRD digest: `sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92`
- Repo scope digest: `sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0`

## Spec path

`docs/specification/product/INIT-REALWORLD-002-api.md`

## Summary

- 23 REQs covering CAP-01..CAP-04 as API provider for CTR-01..CTR-04
- Author subscription + denial-honest empties + subscription-stream lifecycle; web/local out of scope
- Open non-blocking engineering questions: Q-06, Q-07, Q-11, Q-12

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

- PRD: `realworld-meta/prd/INIT-REALWORLD-002.md`
- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/8
- Spec PR: pending
- Service profile: not present (`docs/specification/product/00-service-profile.md` absent)

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-draft
  outcome: pass
  artifact:
    path: docs/specification/product/INIT-REALWORLD-002-api.md
  blockers: []
  signals:
    pr_ready: true
    draft_verdict: PASS
    map_revision: 1
    meta_pr: https://github.com/drivestream-lab/realworld-meta/pull/8
    meta_pr_approved_head: ee9fe45ad23d988eface7517a3a65a7b58b592c1
    prd_digest: sha256:5a9b49dd102202262edca3cb3d2bf315f43782884372d945be9274124b974c92
    scope_digest: sha256:be0c01c3cff0ebd26fabd21761bac6c5f1b10baf4859e82be947b590879e5bd0
    open_non_blocking_questions:
      - Q-06
      - Q-07
      - Q-11
      - Q-12
  next_candidates:
    - spec-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-002] Spec — realworld-api"
    body_path: docs/specification/product/INIT-REALWORLD-002-api.md
```
