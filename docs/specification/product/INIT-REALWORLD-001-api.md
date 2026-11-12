# INIT-REALWORLD-001 — spec slice for realworld-api

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-001 |
| PRD | `realworld-meta/prd/INIT-REALWORLD-001.md` |
| PRD digest (H1) | `sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4` |
| Meta PR | https://github.com/drivestream-lab/realworld-meta/pull/5 |
| Meta PR approved head (G1) | `a500df8eeefbea095ecdd65e00edb128416c3cf4` |
| Impact map | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-001.md` |
| Impact-map revision (H3) | `1` |
| Repo scope digest (H2) | `sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d` |
| Tech-lead approval | Review `PRR_kwDOVac9Rs8AAAABW9LPzQ` / id `5835509709` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T01:45:11Z`; `commit_id` = `a500df8eeefbea095ecdd65e00edb128416c3cf4` (matches merged meta PR #5 head; label `impact-map-lgtm`) |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-11 |
| Status | Draft — dev review required before Forge publish |

> **H4 citations:** The H1–H3 (and G1) rows above are the durable authority
> carrier for mid-lane freshness. Feas / TDD / plan digests are walk-time only
> and may be purged at initiative closure — see
> `prayog-skills/references/artifact-write-contract.md`.

## Overview

`realworld-api` is the **provider** for CAP-01..CAP-06 and CTR-01..CTR-06: public bulletin read without a seat; contribution-seat lifecycle (register eligibility, login seat, logout unseat, re-login reseat); seated tagged markdown publish with immediate visibility; own-article revise/delete; private favorites shelf with inter-member isolation; own nameplate self-update — all with fail-closed denial for unseated and peer-attack paths.

**Out of this repo:** Wave0a UAT chrome and kill-path driving (`realworld-web`); local compose prove environment (`realworld-local`); comments, follows, personalized feeds, OAuth, public who-favorited proof, drafts/moderation, password recovery, account deletion, admin roles.

**Ownership:** this spec states observable API product behavior, acceptance, field meaning, invariants, errors, and compatibility only. Implementation architecture (chassis under `app/` vs `src/`, persistence, transport encoding) is **not** decided here — routed to feasibility / technical review.

## Functional requirements

| ID | Requirement | PRD source | Condition / event | Observable result | Evidence layer |
|----|-------------|-----------|-------------------|-------------------|----------------|
| REQ-01 | Expose a global published-article listing without requiring a contribution seat | PRD REQ-01 / CAP-01 | Guest (no authenticated seat) requests the global feed | Listing state returned (populated or empty); no account wall / auth challenge required for this read | live (CAP-01, J-01) |
| REQ-02 | Expose a single published article without a contribution seat | PRD REQ-02 / CAP-01 | Guest requests a published article that exists | Full published content returned while still unseated | live (CAP-01, J-01) |
| REQ-03 | Expose a tag-filtered published listing without a contribution seat | PRD REQ-03 / CAP-01 | Guest requests a tag lane | Only currently tagged published articles for that tag (or empty lane) | live (CAP-01, J-02) |
| REQ-04 | Expose a public profile and that author’s published articles without a contribution seat | PRD REQ-04 / CAP-01 | Guest requests an existing member’s public profile | Public presentation visible; author’s published articles discoverable (list may be empty) | live (CAP-01, J-03) |
| REQ-05 | Support tag-hop discovery from a published article’s tags | PRD REQ-05 / CAP-01 | Guest, reading an article, requests a tag lane for one of its tags | Lane for that tag returned; other matching articles openable when present | live (CAP-01, J-04) |
| REQ-06 | Place a multi-tagged article in every matching tag lane | PRD REQ-06 / CAP-01 | Published article carries ≥2 tags; Guest requests each tag lane | Same article appears in each lane for its current tags | live (CAP-01, J-04) |
| REQ-07 | Keep bulletin reads available after unseat | PRD REQ-07 / CAP-01 | Member logs out, then requests global feed and a published article (including one they authored) | Feed and article readable; no seat required | live (CAP-01, J-17) |
| REQ-08 | Register membership eligibility with unique username, unique email, and password | PRD REQ-08 / CAP-02; IM-01 / OQ-01 default | Visitor submits registration with unique username + unique email + password | Membership record exists; actor can obtain a seat via login; bio/image not required at register | live (CAP-02, J-05) |
| REQ-09 | Refuse registration that collides on username or email | PRD REQ-09 / CAP-02 | Visitor registers with a taken username or taken email | No second membership; registration fails closed; no seat from that attempt | unit / live (CAP-02, J-05) |
| REQ-10 | Seat an existing member by authenticating | PRD REQ-10 / CAP-02; IM-04 / OQ-04 default | Registered member submits valid credentials (login) | Authenticated session exists; contribution seat active | live (CAP-02, J-06) |
| REQ-11 | Refuse seating with invalid credentials | PRD REQ-11 / CAP-02 | Actor submits credentials that do not match a membership | No authenticated session; seat inactive | unit / live (CAP-02, J-11) |
| REQ-12 | Unseat on logout and revoke contribution actions | PRD REQ-12 / CAP-02 | Authenticated member logs out | Publish, favorite, and profile self-update unavailable until later successful login; bulletin reading remains available | live (CAP-02, J-07) |
| REQ-13 | Reseat after re-login | PRD REQ-13 / CAP-02 | Previously logged-out member authenticates again with valid credentials | Publish, favorite, and profile self-update available again | live (CAP-02, J-07) |
| REQ-14 | Deny contribution actions while unseated as a product rule | PRD REQ-14 / CAP-02 | Guest or post-logout actor attempts publish, favorite/unfavorite, or profile self-update | Each attempt fails closed; no new article, no shelf change, no profile change | live (CAP-02, J-08) |
| REQ-15 | Publish a tagged markdown article with immediate visibility | PRD REQ-15 / CAP-03 | Seated member publishes markdown body with ≥1 non-blank tag | Article immediately visible in global feed and each tag lane; Guests can open it; appears among author’s public-profile articles | live (CAP-03, J-06) |
| REQ-16 | Refuse publish when zero non-blank tags are provided | PRD REQ-16 / CAP-03; IM-02 / OQ-02 default | Seated member attempts publish with no tags or only blank tags | No new published article appears | unit / live (CAP-03, J-06) |
| REQ-17 | Bootstrap an empty bulletin via first seated publish | PRD REQ-17 / CAP-03 | Bulletin has zero published articles; seated member publishes a tagged article | Guest global feed becomes non-empty; Guest can open that article | live (CAP-03, J-12) |
| REQ-18 | Refuse publish when the actor is unseated | PRD REQ-18 / CAP-03 | Guest or post-logout actor attempts publish | No new published article created | live (CAP-03, J-08) |
| REQ-19 | Leave the bulletin unchanged when compose never successfully publishes | PRD REQ-19 / CAP-03 | Seated member starts composing but abandons or unseats without successful publish | No new published article; no durable server-side draft artifact | live (CAP-03, J-18) |
| REQ-20 | Allow edit of only own published articles | PRD REQ-20 / CAP-04 | Author changes title, body, and/or tags on an article they own | Subsequent reads show updated published content; visibility remains immediate | live (CAP-04, J-09) |
| REQ-21 | Keep tag lanes consistent after tag-set edit | PRD REQ-21 / CAP-04 | Author changes an article’s tags | Article appears in lanes for new tags and no longer in lanes for removed tags | live (CAP-04, J-15) |
| REQ-22 | Refuse an edit that would leave zero non-blank tags | PRD REQ-22 / CAP-04; IM-02 | Author attempts to save an update with an empty / blank-only tag set | Prior published content and tag lanes unchanged | unit / live (CAP-04, J-15) |
| REQ-23 | Allow delete of only own published articles | PRD REQ-23 / CAP-04 | Author deletes an article they own | Article disappears from global feed, tag lanes, and author public-profile list; Guest open-by-reference no longer shows published content | live (CAP-04, J-09) |
| REQ-24 | Refuse edit or delete of another author’s article | PRD REQ-24 / CAP-04 | Peer member attempts to change or remove an article they do not own | That article’s content and bulletin presence unchanged | live (CAP-04, J-10) |
| REQ-25 | Favorite another author’s article onto a private shelf | PRD REQ-25 / CAP-05 | Seated member favorites an article they do not own | Article appears on that member’s private shelf; no public who-favorited social proof emitted | live (CAP-05, J-13) |
| REQ-26 | Unfavorite a previously favorited article | PRD REQ-26 / CAP-05 | Seated member removes a favorite | Article no longer appears on that member’s private shelf | live (CAP-05, J-13) |
| REQ-27 | Keep one member’s private shelf invisible to another member | PRD REQ-27 / CAP-05 | Member A has favorited; Member B is seated and is not A | Member B cannot inspect A’s private shelf | live (CAP-05, J-16) |
| REQ-28 | Refuse favorite of own article | PRD REQ-28 / CAP-05 | Seated member attempts to favorite an article they authored | Private shelf unchanged for that attempt | unit / live (CAP-05, J-13) |
| REQ-29 | Deny favorite actions after unseat | PRD REQ-29 / CAP-05 | Post-logout actor attempts favorite/unfavorite | Private shelf unchanged | live (CAP-05, J-07) |
| REQ-30 | Update own nameplate editable fields so public readers see the change | PRD REQ-30 / CAP-06; IM-03 / OQ-03 default | Seated member changes bio and/or image (username/email identity-locked) | Subsequent public-profile views show updated bio/image; username/email unchanged by self-update | live (CAP-06, J-13) |
| REQ-31 | Refuse update of another member’s nameplate | PRD REQ-31 / CAP-06 | Peer member attempts to change Member A’s profile | A’s public profile unchanged | live (CAP-06, J-19) |
| REQ-32 | Deny nameplate self-update after unseat | PRD REQ-32 / CAP-06 | Post-logout actor attempts profile self-update | Profile unchanged | live (CAP-06, J-07) |
| REQ-33 | Prevent private-shelf pointers from resurrecting a deleted article’s public readability | PRD REQ-33 / CAP-05; IM-08 / OQ-08 default | Author deletes a published article that still has (or had) a shelf pointer | Shelf must not expose deleted article body; Guest open-by-reference returns stable not-found (no prior body) | live (CAP-05, J-09) |
| REQ-34 | Order the global feed newest-first by publish/update time | PRD OQ-06 / IM-06 default; CAP-01 | Guest or member requests the global feed with ≥2 published articles | Listing order is newest-first by the article’s publish/update time | integration / live (CAP-01, J-01) |
| REQ-35 | Fail closed when favoriting a missing or already-deleted article | PRD OQ-07 / IM-07 default; CAP-05 | Seated member attempts to favorite a missing or deleted article | Fail closed (not-found); private shelf unchanged | unit / live (CAP-05, J-13) |

> **Id convention:** `REQ-*` is canonical. Legacy display alias `FR-{nn}` ≡ `REQ-{nn}` — prefer `REQ-*`.
>
> **Behavioral acceptance vs evidence:** Condition/event + observable result are
> the product acceptance statement (implementation-neutral). Evidence layer
> names how it will be proved later. Live evidence cites `CAP-*` and/or `J-*`.

## Capabilities (carried from PRD)

| ID | Capability | Journeys | Notes |
|----|------------|----------|-------|
| CAP-01 | Public bulletin reading | J-01, J-02, J-03, J-04, J-12, J-14, J-17 | Provider of CTR-01; never requires a seat |
| CAP-02 | Contribution seat lifecycle | J-05, J-06, J-07, J-08, J-11, J-14, J-17, J-18 | Provider of CTR-02; register≠seat (IM-04) |
| CAP-03 | Seated bulletin contribution | J-06, J-08, J-12, J-14, J-18 | Provider of CTR-03; ≥1 non-blank tag |
| CAP-04 | Seated own-work revision | J-09, J-10, J-15 | Provider of CTR-04 |
| CAP-05 | Private shelf | J-07, J-08, J-09, J-13, J-16 | Provider of CTR-05; no public social proof |
| CAP-06 | Own nameplate | J-07, J-08, J-13, J-19 | Provider of CTR-06; bio/image editable |

## Journeys (carried from PRD)

| ID | Actor | Trigger | Main flow | Primary edge | Abandon | Caps |
|----|-------|---------|-----------|--------------|---------|------|
| J-01 | Guest | Wants published content | Opens global feed → opens article when present → reads | Empty bulletin → empty ungated feed | Leaves without registering | CAP-01 |
| J-02 | Guest | Follows a topic | Opens tag lane → opens matching article | Empty tag lane for that tag only | Leaves lane | CAP-01 |
| J-03 | Guest | Curious about an author | Opens public profile → opens author’s article when present | Profile with zero articles | Leaves profile | CAP-01 |
| J-04 | Guest | Continues discovery across tags | Multi-tagged article → each tag lane → confirms membership | Sole article in a lane | Stops after one hop | CAP-01 |
| J-05 | Visitor → eligible member | Decides to join | Registers unique identity → membership exists → logs in (IM-04) | Duplicate identity refused | Abandons; remains Guest | CAP-02 |
| J-06 | Seated member | Puts writing on bulletin | Authenticates → publishes tagged markdown → Guest sees it | Zero tags → refuse | Unseat before publish; no article | CAP-02, CAP-03 |
| J-07 | Seated → Guest → Seated | Ends then resumes seat | Logout → contribution denied → read still works → login → contribution works | Stale seat must not mutate while unseated | N/A | CAP-02, CAP-05, CAP-06 |
| J-08 | Guest | Probes the seat | Attempts publish, favorite, profile self-update while unseated | Each fails closed; no side effects | Registers (J-05) | CAP-02, CAP-03, CAP-05, CAP-06 |
| J-09 | Author | Fixes or removes own writing | Edits and/or deletes own article | After delete, Guest not-found; shelf must not resurrect (REQ-33) | Cancels edit; prior remains | CAP-04, CAP-05 |
| J-10 | Peer member | Attacks ownership | Attempts edit/delete on another’s article | Bulletin unchanged | Returns to own work | CAP-04 |
| J-11 | Member | Valid vs invalid seating | Good login seats; bad credentials refused | Invalid login leaves seat inactive | Stops trying | CAP-02 |
| J-12 | Seated + Guest | Bootstraps empty bulletin | First tagged publish → Guest feed non-empty → Guest opens | Failed publish leaves empty ungated feed | Abandon compose; empty remains | CAP-01, CAP-03 |
| J-13 | Seated member | Private shelf + nameplate | Favorite others → shelf → unfavorite; update bio/image → Guest sees | Favorite own → refused | Leaves unused / cancels | CAP-05, CAP-06 |
| J-14 | Guest → Seated | Converts mid-read | Guest reads → registers → logs in → publishes | Contribution unavailable until seated | Abandons join; still reads | CAP-01, CAP-02, CAP-03 |
| J-15 | Author | Retags published writing | Edits tag set → lane membership moves; empty tag set refused | Old lane no longer lists article | Cancels; prior tags remain | CAP-04 |
| J-16 | Peer member | Probes shelf privacy | A favorites; B attempts to inspect A’s shelf | B cannot see A’s shelf | B favorites into B’s own shelf | CAP-05 |
| J-17 | Former seated (now Guest) | Confirms bulletin after unseat | Logout → feed → open own prior article as Guest | Contribution still fail-closed | Leaves without reseating | CAP-01, CAP-02 |
| J-18 | Seated member | Abandons / unseats mid-compose | Starts compose → abandon or logout without publish | No published article; no server draft | N/A | CAP-02, CAP-03 |
| J-19 | Peer member | Attacks nameplate ownership | Attempts to change another’s profile | Target unchanged | Returns to own nameplate | CAP-06 |

## Negative and failure paths

| REQ | Condition | Required behavior | Why it matters | Evidence |
|-----|-----------|-------------------|----------------|----------|
| REQ-01 | Bulletin has zero articles | Empty feed; still no account wall | Open bulletin ≠ must have content | live (J-01, J-12) |
| REQ-03 | Tag with no articles | Empty lane for that tag only | Prevents false discovery | live (J-02) |
| REQ-07 | After logout, actor reads own prior article | Readable as Guest; contribution still denied | Separates bulletin openness from seat | live (J-17) |
| REQ-09 | Duplicate registration identity | Fail closed; no second membership; no seat | Eligibility integrity | unit / live (J-05) |
| REQ-11 | Invalid credentials | No seat; contribution stays off | Protects seat gate | unit / live (J-11) |
| REQ-12 | After logout | Contribution unavailable; reading still works | Kill assumption — unseat | live (J-07) |
| REQ-14 / REQ-18 | Unseated contribution cluster | Fail closed; no side effects | Kill assumption — product rule not chrome | live (J-08) |
| REQ-16 / REQ-22 | Zero-tag create or edit | No create; no destructive empty-tag save | Tagged-article lock | unit / live |
| REQ-19 | Abandon / unseat mid-compose | Bulletin unchanged; no draft artifact | No-draft lock | live (J-18) |
| REQ-24 | Cross-author mutate | Bulletin unchanged | Ownership integrity | live (J-10) |
| REQ-27 | Peer views another’s shelf | Isolation holds | Privacy beyond “no public proof” | live (J-16) |
| REQ-28 | Favorite own article | Refused; shelf unchanged | Lock 10 | unit / live (J-13) |
| REQ-29 / REQ-32 | Post-logout shelf/nameplate | No mutation | Kill assumption — unseat on personal surfaces | live (J-07) |
| REQ-31 | Peer nameplate attack | Target profile unchanged | Nameplate ownership | live (J-19) |
| REQ-33 / REQ-35 | Deleted / missing article + shelf | Not-found; no body resurrection; shelf unchanged on favorite miss | Prevents ghost public content | live / unit |
| J-05 abandon | Visitor abandons registration | Remains Guest; no partial seat | Avoid half-open seat | live (J-05) |

## Out of scope for this repo

- Wave0a web UAT chrome, client navigation, and kill-path driving — **realworld-web**
- Local compose / DB join for live prove — **realworld-local**
- Comments (legacy route may exist in source; not a Wave0a CAP/REQ)
- Follow / unfollow graphs or follower counts
- Personalized / “your feed” timelines
- Email verification gates; OAuth / third-party identity
- Public who-favorited social proof (counts or actor lists)
- Draft or moderation queues; durable server-side drafts
- Password reset / recovery; account deletion / data-export programmes
- Admin / moderator / staff tooling
- Multi-device session cascade beyond “explicit logout unseats *this* session” (OQ-05 / IM-05 deferred)
- Mid-read live push after delete (OQ-09 / IM-09 deferred — next navigation / reopen sufficient)

## Cross-service contracts

| Contract ID | Provider / owner | Consumer / owner | Entry point | Input shape | Output shape | Invariants | Errors | Compatibility / versioning | Contract-test location |
|-------------|------------------|------------------|-------------|-------------|--------------|------------|--------|----------------------------|------------------------|
| CTR-01 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Read the public bulletin | Identity of listing mode (global / tag / author), article reference, profile username | Global listing, tag-filtered listing, single published article, public profile (+ author’s published articles); empty sets allowed | Only published articles appear; Guests may read; multi-tag articles belong to every listed tag’s set; no draft/moderation states; reading never requires a seat; feed order newest-first (REQ-34) | Missing article → stable not-found; empty sets allowed | New Wave0a seam; breaking change requires INIT revision | planned under `tests/verify` / consumer contract suite (TBD in plan) |
| CTR-02 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Manage the contribution seat | Register: unique username + unique email + password; authenticate credentials; logout signal | Eligibility confirmation; seated session proof; unseated state after logout | Contribution actions require a valid seat; bulletin reading never requires a seat; register creates eligibility only (IM-04); unseat and reseat both observable | Duplicate identity; invalid credentials; malformed required fields; session already absent → treat as unseated | New Wave0a seam | planned under `tests/verify` (TBD in plan) |
| CTR-03 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Contribute to the bulletin | Create own markdown article with ≥1 non-blank tag | Newly published article identity + fields; immediate listing membership | Seat required; zero/blank tags rejected; abandon/unseat without success creates nothing; no server draft | Unauthenticated; zero tags | New Wave0a seam | planned under `tests/verify` (TBD in plan) |
| CTR-04 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Revise own bulletin work | Update/delete own article; optional tag-set on update | Updated article or deletion confirmation; lane membership reflects current tags | Ownership required; zero/blank tags rejected on tag-set updates; peer mutate denied | Unauthenticated; not owner; zero tags; missing article | New Wave0a seam | planned under `tests/verify` (TBD in plan) |
| CTR-05 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Maintain private shelf | Favorite/unfavorite target article reference; request own shelf | Own private shelf listing; mutation confirmation | Shelf private and isolated across members; no who-favorited social proof; unseated denied; own-article favorite denied; shelf must not resurrect deleted body (REQ-33); missing/deleted favorite fails closed (REQ-35) | Unauthenticated; own article; missing article; peer inspection denied; deleted article | New Wave0a seam | planned under `tests/verify` (TBD in plan) |
| CTR-06 | realworld-api / @drivestream-lab/backend-devs | realworld-web / @drivestream-lab/frontend-devs | Maintain own nameplate | Self-update bio and/or image; public profile read by username | Updated public profile fields; public read of nameplate + author’s articles | Only owner may update; unseated denied; peer update denied; username/email identity-locked on self-update; updates reflected on subsequent public reads | Unauthenticated; not owner | New Wave0a seam | planned under `tests/verify` (TBD in plan) |

## Non-functional requirements

| Area | Requirement or N/A rationale | Acceptance / evidence |
|------|------------------------------|-----------------------|
| Security | Contribution seat must keep publish / favorite / profile self-update closed to Guests and post-logout actors as a product rule (REQ-12, REQ-14, REQ-18, REQ-29, REQ-32). Credential verification fail-closed (REQ-11). Peer nameplate mutation denied (REQ-31). No OAuth in this INIT. | unit + live seat-denial paths |
| Reliability | N/A beyond fail-closed UAT behavior — not a multi-region SLA INIT. Incomplete actions must not leave partial publish / shelf / nameplate success. | inspection / negative-path tests |
| Performance / capacity | N/A for Wave0a UAT scale; no concurrent-load target locked. | N/A |
| Observability | N/A as product kill criterion; operational logging remains an engineering concern (chassis rules). | N/A for product acceptance |
| Privacy / data handling | Private shelves isolated across members (REQ-25, REQ-27). No public who-favorited proof. Shelf must not resurrect deleted articles (REQ-33). Nameplate exposes bio/image as public; username/email identity-locked. | live (J-13, J-16) |
| Migration / compatibility | Clean-slate Wave0a — no prior tenant corpus migration required. Legacy Conduit-shaped code under `app/` is baseline source, not a guaranteed as-built product surface until proven. | as-built / feasibility |
| Rollback / recovery | N/A as product REQ — delivery rollback is engineering. | N/A |
| Operations / support | Live prove environment is `realworld-local` compose (out of this repo); no 24×7 support envelope locked. | N/A in-repo |

## Assumptions

| ID | Assumption | Evidence | Owner | Status | Invalidated when |
|----|------------|----------|-------|--------|------------------|
| A-01 | Registration uniqueness covers username and email both unique | PRD A-01; IM-01 default | PM | confirmed (Wave0a default applied) | OQ-01 reopened with different uniqueness set |
| A-02 | Markdown is the authored body format; readable published content is the kill bar | PRD A-02 | PM | confirmed | Rich media beyond markdown becomes in-scope |
| A-03 | Author delete removes public bulletin presence; shelf must not resurrect public readability | PRD A-03; IM-08 | PM | confirmed | Public resurrection via shelf allowed (would break REQ-33) |
| A-04 | Explicit logout defines unseat for Wave0a; idle-timeout not required | PRD A-04 | PM | confirmed | Idle timeout becomes a kill criterion |
| A-05 | Tags are author-chosen free-form labels; blank tokens rejected; ≥1 non-blank required | PRD A-05; IM-02 | PM | confirmed | Curated taxonomy replaces free-form |
| A-06 | Reseat on successful re-authentication is in scope | PRD A-06 | PM | confirmed | Reseat removed from kill path |
| A-07 | Inter-member shelf isolation is required | PRD A-07 | PM | confirmed | Privacy redefined as “no public proof” only |
| A-08 | Unfinished compose has no durable server-side draft | PRD A-08 | PM | confirmed | Server drafts become in-scope |
| A-09 | As-built index is absent; source under `app/` is a legacy Conduit FastAPI example (includes out-of-scope comments) | Source scan 2026-11-11; empty `docs/specification/as-built/` | PE | open | As-built index published with capability rows |

## Spec questions (ambiguities — need PM or domain confirmation before feasibility)

| ID | Lane | Question | Owner | Blocking | Required by | Default if deferred | Status | Resolution link |
|----|------|----------|-------|----------|-------------|---------------------|--------|-----------------|
| Q-01 | PM | Registration field/uniqueness set (OQ-01 / IM-01) | PM | no | feasibility | Unique username + unique email + password; bio/image via nameplate | resolved | Impact-Map IM-01 default → REQ-08/REQ-09 |
| Q-02 | PM | Tag normalization limits (OQ-02 / IM-02) | PM | no | feasibility | Free-form; reject blank; ≥1 non-blank tag | resolved | Impact-Map IM-02 default → REQ-16/REQ-22 |
| Q-03 | PM | Nameplate editable vs identity-locked (OQ-03 / IM-03) | PM | no | feasibility | Bio/image editable; username/email locked | resolved | Impact-Map IM-03 default → REQ-30 |
| Q-04 | PM | Register-may-seat vs login-required (OQ-04 / IM-04) | PM | no | feasibility | Eligibility only; login before contribution | resolved | Impact-Map IM-04 default → REQ-08/REQ-10 |
| Q-05 | PE | Multi-session logout cascade (OQ-05 / IM-05) | PE | no | later | Unseat logging-out session only | open | Impact-Map IM-05; revisit if multi-device UAT added |
| Q-06 | PM | Global feed ordering (OQ-06 / IM-06) | PM | no | feasibility | Newest-first by publish/update time | resolved | Impact-Map IM-06 default → REQ-34 |
| Q-07 | PM | Favorite missing/deleted article (OQ-07 / IM-07) | PM | no | feasibility | Fail closed; shelf unchanged | resolved | Impact-Map IM-07 default → REQ-35 |
| Q-08 | PM | Guest open-by-reference after delete (OQ-08 / IM-08) | PM | no | feasibility | Stable not-found; no prior body | resolved | Impact-Map IM-08 default → REQ-33 |
| Q-09 | PE | Mid-read refresh vs next navigation after delete (OQ-09 / IM-09) | PE | no | later | Next navigation / reopen sufficient | open | Impact-Map IM-09; API emits not-found on reopen |
| Q-10 | PE | How to treat legacy Conduit `app/` (incl. comments routes) vs Wave0a chassis under platform `src/` rules | PE | no | technical review | Satisfy REQs regardless of chassis; do not expand Wave0a to comments; architecture chosen in TDD/ADR | open | Feasibility / technical review |

## Draft check summary (D1–D12)

| Check | Status | Evidence / findings |
|-------|--------|---------------------|
| D1 Approved handoff current | PASS | H1 digest matches PRD file; H3 map_revision=1; H2 api scope digest present; G1 APPROVED review `commit_id` = meta PR #5 head `a500df8e…`; label `impact-map-lgtm`; repo affected not deferred |
| D1b No open blocking IM-* | PASS | Impact-map §10: no `Blocking: yes` open rows; IM-01..IM-04, IM-06..IM-08 defaults applied into REQs |
| D2 Complete PRD traceability | PASS | CAP-01..CAP-06 each have ≥1 REQ; every REQ cites PRD CAP/REQ or OQ/IM default |
| D2b Journeys carried | PASS | J-01..J-19 carried; live evidence cites CAP/J |
| D3 Repo-bounded scope | PASS | Provider scope matches impact-map H2; web/local and non-goals listed under Out of scope |
| D4 Observable acceptance | PASS | Each REQ has condition/event, observable result, evidence layer; implementation-neutral |
| D5 Negative/failure paths | PASS | Table covers unseated, ownership, zero-tag, shelf privacy, delete/not-found, abandon |
| D6 Assumptions/questions | PASS | Assumptions evidenced; questions have lane/owner/blocking/default/status; material PM defaults applied |
| D7 Cross-repository contracts | PASS | CTR-01..CTR-06 semantic seams with provider=api, consumer=web |
| D8 NFR applicability | PASS | All eight areas specified or N/A with reason |
| D9 As-built alignment | PASS | As-built index absent; source scan notes legacy Conduit under `app/` (existing baseline) vs Wave0a CAP/REQ obligations (new prove surface); comments present in source but out of scope |
| D10 Dependency order | PASS | Matches impact-map: api → web → local; api depends on none |
| D11 Zero unresolved blockers | PASS | No blocking Q remaining; Q-05/Q-09/Q-10 non-blocking with defaults |
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
| Existing spec PR | none open (historical CLOSED: https://github.com/drivestream-lab/realworld-api/pull/2) |
| Proposed branch | `chore/INIT-REALWORLD-001-spec-realworld-api` |
| Proposed base | `develop` |
| Proposed title | `[INIT-REALWORLD-001] Spec — realworld-api` |
| PR type | **Draft** (entire spec lifecycle) |
| Local artifacts to publish | `docs/specification/product/INIT-REALWORLD-001-api.md`, `docs/specification/README.md` |
| Forge readiness | fill `handoff.forge` for `open_draft_pr`; recommend `/commit-workspace` then `/open-draft-pr` — do not commit/push/open PR inside this skill |
| Reviewer | @drivestream-lab/backend-devs |
| Initial Gate 2 label | `spec-pending` |
| Additional invalidation label | none |
| Blocking items | none |

**No GitHub side effects have occurred.** Persist the draft locally; Forge publish is a later `/commit-workspace` / `/open-draft-pr` or Gateflow ForgeClient step.

### Proposed Draft PR body

```markdown
## Initiative

INIT-REALWORLD-001 — Public bulletin with session-bound contribution seat

## Meta handoff

- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/5
- Approved meta head: `a500df8eeefbea095ecdd65e00edb128416c3cf4`
- Impact-map revision: 1
- PRD digest: `sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4`
- Repo scope digest: `sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d`

## Spec path

`docs/specification/product/INIT-REALWORLD-001-api.md`

## Summary

- 35 REQs covering CAP-01..CAP-06 as API provider for CTR-01..CTR-06
- Wave0a seat/bulletin/shelf/nameplate fail-closed paths; web/local out of scope
- Open non-blocking engineering questions: Q-05, Q-09, Q-10

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

- PRD: `realworld-meta/prd/INIT-REALWORLD-001.md`
- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/5
- Spec PR: pending
- Service profile: not present (`docs/specification/product/00-service-profile.md` absent)

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-draft
  outcome: pass
  artifact:
    path: docs/specification/product/INIT-REALWORLD-001-api.md
  blockers: []
  signals:
    pr_ready: true
    draft_verdict: PASS
    map_revision: 1
    meta_pr: https://github.com/drivestream-lab/realworld-meta/pull/5
    meta_pr_approved_head: a500df8eeefbea095ecdd65e00edb128416c3cf4
    prd_digest: sha256:cdc1f66d5cf4c1f12fd0f9ed8bf28d320d4aef941d6abbb0612f53886a1fcfb4
    scope_digest: sha256:cc140afde9cf417ae055bab1bd673579edbc510e09ce1c950203abfbe2b4ba4d
    open_non_blocking_questions:
      - Q-05
      - Q-09
      - Q-10
  next_candidates:
    - spec-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-001] Spec — realworld-api"
    body_path: docs/specification/product/INIT-REALWORLD-001-api.md
```
