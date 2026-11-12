# INIT-REALWORLD-003 — spec slice for realworld-api

| Field | Value |
|-------|-------|
| Initiative | INIT-REALWORLD-003 |
| PRD | `realworld-meta/prd/INIT-REALWORLD-003.md` |
| PRD digest (H1) | `sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8` |
| Meta PR | https://github.com/drivestream-lab/realworld-meta/pull/10 |
| Meta PR approved head (G1) | `abfbbcff877a83c298776fd4801b8ac4c75ddfba` |
| Impact map | `realworld-meta/prd/reports/Impact-Map-INIT-REALWORLD-003.md` |
| Impact-map revision (H3) | `1` |
| Repo scope digest (H2) | `sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7` |
| Tech-lead approval | Review `PRR_kwDOVac9Rs8AAAABXCDSZQ` / id `5840622181` by `adh-reviewer[bot]` (Gate‑1 attestation by adh.pe), APPROVED at `2026-11-10T10:48:57Z`; `commit_id` = `abfbbcff877a83c298776fd4801b8ac4c75ddfba` (matches merged meta PR #10 head; label `impact-map-lgtm`) |
| Repo | drivestream-lab/realworld-api |
| Date | 2026-11-12 |
| Status | Draft — dev review required before Forge publish |

> **H4 citations:** The H1–H3 (and G1) rows above are the durable authority
> carrier for mid-lane freshness. Feas / TDD / plan digests are walk-time only
> and may be purged at initiative closure — see
> `prayog-skills/references/artifact-write-contract.md`.

## Overview

`realworld-api` is the **provider** for CAP-01..CAP-03 and REQ-01..REQ-16: seated owner-private park / recall / relabel / discard of replay-ready personal search intents with query-string fidelity on owner recall; refuse empty/whitespace parks; durable membership retention across unseat/reseat; fail-closed unseated and peer isolation — all proven on the machine-consumable API surface (no web UI this INIT).

**Out of this repo:** Settings / any web UI for parked-search stewardship (`realworld-web`); local compose/env delta for prove hosting (`realworld-local`); share/public/collaborative parks; auto-running parked queries; new article-search ranking; reopening INIT-REALWORLD-001 favorites/nameplate or INIT-REALWORLD-002 subscription rules; comments; OAuth; email verification; mobile/native clients; admin tooling over other members’ parks.

**Ownership:** this spec states observable API product behavior, acceptance, field meaning, invariants, errors, and compatibility only. Implementation architecture (persistence shape, route encoding, chassis under `app/` vs `src/`) is **not** decided here — routed to feasibility / technical review.

**Baseline:** INIT-REALWORLD-001 seat rules remain the gate for “signed-in reader.” INIT-001 favorites and INIT-002 author subscriptions are **not** reopened. Parked search memory is a separate private retention object. Source scan finds **no** existing saved-search / park tables or routes under `app/` — this INIT introduces a new prove surface.

## Functional requirements

| ID | Requirement | PRD source | Condition / event | Observable result | Evidence layer |
|----|-------------|-----------|-------------------|-------------------|----------------|
| REQ-01 | Park a search intent with a mnemonic label | PRD REQ-01 / CAP-01 | Seated member parks a non-empty query string and a non-empty mnemonic label | An owner-private park exists with that exact query string and that label; owner recall shows both | live (CAP-01, J-01) |
| REQ-02 | Park a search intent without a label | PRD REQ-02 / CAP-01; IM-04 / OQ-04 default | Seated member parks a non-empty query string and omits a label, or supplies a blank/whitespace-only label | An owner-private park exists with that exact query string and no label; owner recall shows the unlabeled park | live (CAP-01, J-02) |
| REQ-03 | Refuse park of empty or whitespace-only query text | PRD REQ-03 / CAP-01 | Seated member attempts to park empty or whitespace-only query text | No park is created; owner recall unchanged by that attempt | live (CAP-01, J-12) |
| REQ-04 | Refuse park while unseated | PRD REQ-04 / CAP-03 | Guest or post-logout actor attempts to park a search intent | No new park is created for any membership | live (CAP-03, J-07) |
| REQ-05 | Recall only the owner’s parks with query fidelity | PRD REQ-05 / CAP-02 | Seated member requests their search-memory list when they own zero or more parks | List contains exactly that member’s parks (or empty); each listed park presents its retained query string (and label if any); no other member’s parks appear | live (CAP-02, J-03) |
| REQ-06 | Relabel an owned park (including clear-to-none) | PRD REQ-06 / CAP-02; IM-07 / OQ-07 default; IM-01 / OQ-01 default | Seated member changes the mnemonic label on a park they own (new label, or clear to no label); does not change the parked query string | Subsequent owner recall shows the updated label (or no label); retained query string unchanged | live (CAP-02, J-04) |
| REQ-07 | Discard an owned park | PRD REQ-07 / CAP-02 | Seated member discards a park they own | That park no longer appears on the owner’s recall list | live (CAP-02, J-05) |
| REQ-08 | Persist parks across unseat and reseat | PRD REQ-08 / CAP-02 | Seated member parks an intent, logs out, then logs in again without changing parks while unseated | After reseat, owner recall still includes that park with the same query string | live (CAP-02, J-08) |
| REQ-09 | Allow empty own-recall after the last discard | PRD REQ-09 / CAP-02 | Seated member discards their last remaining park | Owner recall list is empty and valid (not an error wall) | live (CAP-02, J-10) |
| REQ-10 | Keep one member’s parks invisible to another seated member | PRD REQ-10 / CAP-03 | Member A owns ≥1 park; Member B is seated and is not A | B cannot obtain A’s park contents (including query text) via list or direct access | live (CAP-03, J-06) |
| REQ-11 | Refuse relabel or discard of another member’s park | PRD REQ-11 / CAP-03 | Seated peer attempts to relabel or discard Member A’s park | A’s park unchanged; peer’s own recall unchanged by that attempt | live (CAP-03, J-09) |
| REQ-12 | Deny list / relabel / discard while unseated | PRD REQ-12 / CAP-03 | Guest or post-logout actor attempts list, relabel, or discard | No park contents of any member are disclosed as a successful recall result; no relabel/discard side effects | live (CAP-03, J-07) |
| REQ-13 | Refuse mutate of a missing or non-owned park identity | PRD REQ-13 / CAP-03; IM-03 / OQ-03 default | Seated member attempts relabel or discard against a park identity that does not exist for them (missing or peer-owned) | Own recall unchanged; fail closed as indistinguishable not-found to the requester; no park contents disclosed | unit / live (CAP-03, J-11) |
| REQ-14 | Order owner recall newest-first by park time | PRD OQ-05 / IM-05 default; CAP-02 | Seated member requests own recall with ≥2 parks | Parks are ordered newest-first by park time; exact timestamp source left to engineering | integration / live (CAP-02, J-03) |
| REQ-15 | Allow duplicate query strings and non-unique labels per owner | PRD OQ-06 / IM-06 default; CAP-01 / CAP-02 | Seated member parks the same non-empty query string more than once (labels may match or differ) | Distinct parks exist; owner recall includes each; labels need not be unique per owner | live (CAP-01, CAP-02, J-01) |
| REQ-16 | Keep parked query string immutable after park | PRD OQ-01 / IM-01 default; CAP-02 | Seated member attempts stewardship after park | Mutate paths this INIT are relabel and discard only; retained query string is not replaced via an in-scope edit path | unit / live (CAP-02, J-04) |

> **Id convention:** `REQ-*` is canonical (`prayog-skills/references/id-conventions.md`).
> Legacy display alias `FR-{nn}` ≡ `REQ-{nn}` — prefer `REQ-*`.
>
> **Behavioral acceptance vs evidence:** Condition/event + observable result are
> the product acceptance statement (implementation-neutral). Evidence layer
> names how it will be proved later. Live evidence cites `CAP-*` and/or `J-*`.

## Capabilities (carried from PRD)

| ID | Capability | Journeys | Notes |
|----|------------|----------|-------|
| CAP-01 | Park a personal search intent | J-01, J-02, J-08, J-12 | Non-empty query + optional mnemonic; seated-only; refuse empty/whitespace; duplicates allowed (REQ-15) |
| CAP-02 | Recall and maintain own search memory | J-01, J-02, J-03, J-04, J-05, J-08, J-10 | List with query fidelity; relabel (incl. clear); discard; empty recall valid; persist across reseat; newest-first (REQ-14); query immutable (REQ-16) |
| CAP-03 | Private continuity isolation | J-06, J-07, J-09, J-11 | Peer opacity (no query harvest); unseated fail-closed; missing/non-owned mutate denied as indistinguishable not-found (REQ-13) |

## Journeys (carried from PRD)

| ID | Actor | Trigger | Main flow | Primary edge | Abandon | Caps |
|----|-------|---------|-----------|--------------|---------|------|
| J-01 | Seated member | Wants to keep a named search intent for later reuse | Parks query + label → recalls → sees same query + label | Duplicate query allowed (REQ-15) | Abandons before park → no park | CAP-01, CAP-02 |
| J-02 | Seated member | Wants to keep a query without naming it | Parks query with no label → recalls → sees unlabeled park with same query | Blank/whitespace label → treated as no label (REQ-02) | Abandons → no park | CAP-01, CAP-02 |
| J-03 | Seated member | Wants to continue a prior search | Opens own recall list and reads retained query text | Empty list when none parked; newest-first when ≥2 (REQ-14) | Leaves without changes | CAP-02 |
| J-04 | Seated member | Wants a clearer mnemonic | Relabels own park → recalls → sees new label; query unchanged | Clear label to none (REQ-06); query remains immutable (REQ-16) | Abandons mid-relabel → prior label remains | CAP-02 |
| J-05 | Seated member | No longer wants a parked intent | Discards own park → recalls → absent | — | — | CAP-02 |
| J-06 | Peer member | Tries to harvest another’s search memory | Attempts to list/access Member A’s parks | Denied / no query disclosure | — | CAP-03 |
| J-07 | Guest / post-logout | Tries stewardship without a seat | Attempts park, list, relabel, or discard | Fail closed; no side effects; no disclosure | — | CAP-03 |
| J-08 | Seated member | Relies on continuity across sessions | Parks intent → logs out → logs in → recalls | Same query text still present | — | CAP-01, CAP-02 |
| J-09 | Peer member | Tries to alter another’s park | Attempts relabel or discard of A’s park | A unchanged | — | CAP-03 |
| J-10 | Seated member | Clears the last park | Discards final park → recalls empty | Empty is valid | — | CAP-02 |
| J-11 | Seated member | Uses a bad park identity | Attempts relabel/discard on missing/non-owned id | Fail closed as indistinguishable not-found; own recall unchanged | — | CAP-03 |
| J-12 | Seated member | Tries to park empty intent | Attempts park with empty/whitespace query | Refused; recall unchanged | — | CAP-01 |

## Negative and failure paths

| REQ | Condition | Required behavior | Why it matters | Evidence |
|-----|-----------|-------------------|----------------|----------|
| REQ-02 / J-02 | Label omitted or blank/whitespace-only | Park still creatable; treated as no label | Optional mnemonic must not become a hidden required field | live (J-02) |
| REQ-03 / J-12 | Empty / whitespace query | Create refused; no park record | Continuity object must carry real query text for later reuse | live (J-12) |
| REQ-05 / J-03 | Owner has zero parks | Empty recall list, still seated-only | Empty ≠ error; matches success “list works” | live (J-03) |
| REQ-05 | Owner has parks | Listed query strings match what was parked | Replay readiness without auto-run | live (J-03) |
| REQ-04 / REQ-12 | Unseated park/list/relabel/discard | Fail closed; no disclosure; no mutations | Kill assumption — seat gate | live (J-07) |
| REQ-10 / J-06 | Peer tries to read owner’s parks | Isolation holds; no query harvest | Kill assumption — unauthorized cannot see others’ saves | live (J-06) |
| REQ-11 / J-09 | Peer tries to relabel/discard owner’s park | Target unchanged | Isolation beyond read opacity | live (J-09) |
| REQ-09 / J-10 | Last park discarded | Empty own-recall allowed | Prevents “must always have one” false rule | live (J-10) |
| REQ-13 / J-11 | Missing / non-owned identity | Indistinguishable not-found; own memory unchanged; no contents disclosed | Prevents cross-owner leakage via guessed identities | unit / live (J-11) |
| REQ-08 / J-08 | Logout then login | Parks still present with same query text | Durable continuity vs session-only memory | live (J-08) |
| REQ-06 / REQ-16 | Relabel attempt | Label may change or clear; query string unchanged | Relabel ≠ query rewrite | live (J-04) |
| REQ-15 | Duplicate park of same query | Both parks retained | Label-as-identity not chosen this INIT | live (J-01) |

## Out of scope for this repo

- Settings (or any) web UI list/management for parked searches — **realworld-web** (deferred per impact map)
- Local compose / env delta for API-only live prove hosting — **realworld-local** (deferred; optional host does not mint a CAP)
- Share / public / collaborative saved searches
- Auto-running a parked query against article search as a required success path (IM-02 / OQ-02 — re-presentable text is enough)
- Inventing a new article-search ranking / relevance / full-text product beyond retaining the query string
- Treating labels as unique slot identities (label-as-identity packaging deferred)
- Reopening INIT-REALWORLD-001 publish / seat / favorites / nameplate requirement sets
- Reopening INIT-REALWORLD-002 author subscription / subscription-stream rules
- Comments, OAuth, email verification, mobile/native clients
- Admin/moderation tooling over other members’ parks
- Cross-member transfer or export programmes
- New infra services beyond the existing catalog

## Cross-service contracts

None — no cross-repository boundary. Stewardship is owned and proven on `realworld-api`; `realworld-web` settings UI is an explicit non-goal; `realworld-meta` carries product truth only (PRD §8; impact-map §6).

## Non-functional requirements

| Area | Requirement or N/A rationale | Acceptance / evidence |
|------|------------------------------|-----------------------|
| Security | Seat-bound stewardship; unseated and peer access fail closed (REQ-04, REQ-10–REQ-13). No share/public surface. Missing/non-owned mutate is indistinguishable not-found (REQ-13). | unit + live denial / isolation paths |
| Reliability | N/A beyond fail-closed park/list/relabel/discard behavior — not a multi-region SLA INIT. Incomplete create must not leave a visible park that disagrees with refusal rules. | inspection / negative-path tests |
| Performance / capacity | N/A for guinea-pig scale; no concurrent-load target locked. Per-member count and max query/label lengths may use eng reasonableness limits (IM-04) without inventing product caps this INIT. | N/A |
| Observability | N/A as product REQ — operational logging remains an engineering concern (chassis rules). | N/A for product acceptance |
| Privacy / data handling | Parks are private to the owning membership; peers and guests must not observe query text or labels (REQ-10, REQ-12). | live (J-06, J-07) |
| Migration / compatibility | Additive private state for existing members; default empty own-recall. Does not migrate or rewrite INIT-001 favorites or INIT-002 subscriptions. | as-built / feasibility |
| Rollback / recovery | N/A as product REQ — delivery rollback is engineering. | N/A |
| Operations / support | No new infra services; prove against existing `realworld-api` (local compose may host prove without expanding product scope to web UI). | N/A in-repo |

## Assumptions

| ID | Assumption | Evidence | Owner | Status | Invalidated when |
|----|------------|----------|-------|--------|------------------|
| A-01 | INIT-REALWORLD-001 contribution-seat semantics (login seats, logout unseats) remain the gate for “signed-in reader” | PRD A-01; sibling spec `INIT-REALWORLD-001-api.md` | PM | confirmed | Lead reopens seat meaning conflicting with this INIT |
| A-02 | Park success does not require the query to match live article hits at save time; fidelity of retained text is enough for replay readiness | PRD A-02; IM-02 default | PM | confirmed | Lead requires save-time search validation or auto-run (OQ-02) |
| A-03 | Relabel is mnemonic-only; query-string edit is not required for this INIT’s kill bar | PRD A-03; IM-01 → REQ-16 | PM | confirmed | Lead requires query edit as a mutate path |
| A-04 | “Unauthorized cannot see others’ saves” includes both guests and peer seated members, not only anonymous actors | PRD A-04; REQ-10 / REQ-12 | PM | confirmed | Lead allows peer visibility of parks |
| A-05 | Durable retention means membership-scoped persistence across logout/login, not merely in-process memory | PRD A-05; REQ-08 | PM | confirmed | Lead wants session-only memory |
| A-06 | Owner recall exposing query text is sufficient continuity proof without a web UI or auto-run this INIT | PRD A-06; impact-map deferred web | PM | confirmed | Lead makes UI or auto-run a kill path |
| A-07 | As-built index is absent; source under `app/` has no saved-search / park tables or routes — CAP-01..CAP-03 are new prove surfaces on the Conduit FastAPI baseline | Source scan 2026-11-12; empty `docs/specification/as-built/` | PE | open | As-built index published with capability rows |

## Spec questions (ambiguities — need PM or domain confirmation before feasibility)

| ID | Lane | Question | Owner | Blocking | Required by | Default if deferred | Status | Resolution link |
|----|------|----------|-------|----------|-------------|---------------------|--------|-----------------|
| Q-01 | PM | May the owner change the retained query string after park? (OQ-01 / IM-01) | PM | no | feasibility | Relabel + discard only; query immutable after park | resolved | Impact-Map IM-01 default → REQ-06 / REQ-16 |
| Q-02 | PM | Must continuity include auto-running the parked query? (OQ-02 / IM-02) | PM | no | later | Re-presentable text enough; auto-run non-goal | resolved | Impact-Map IM-02 default → Out of scope |
| Q-03 | PM | Fail-closed shape for missing vs non-owned park identity (OQ-03 / IM-03) | PM | no | feasibility | Indistinguishable not-found; no contents disclosed | resolved | Impact-Map IM-03 default → REQ-13 |
| Q-04 | PM | Per-member max parks and max query/label lengths (OQ-04 / IM-04) | PM | no | feasibility | Eng reasonableness limits acceptable; blank label = no label | resolved | Impact-Map IM-04 default → REQ-02; length limits eng (NFR Performance) |
| Q-05 | PM | Owner-recall ordering rule (OQ-05 / IM-05) | PM | no | feasibility | Newest-first by park time; timestamp source eng | resolved | Impact-Map IM-05 default → REQ-14 |
| Q-06 | PM | Duplicate query strings / unique labels per owner (OQ-06 / IM-06) | PM | no | feasibility | Duplicates allowed; labels need not be unique | resolved | Impact-Map IM-06 default → REQ-15 |
| Q-07 | PM | Clearing a label (relabel to no label) allowed? (OQ-07 / IM-07) | PM | no | feasibility | Allowed without discarding the park | resolved | Impact-Map IM-07 default → REQ-06 |
| Q-08 | PE | How to introduce park persistence and stewardship routes on the legacy Conduit `app/` baseline vs platform `src/` chassis for CAP-01..CAP-03 | PE | no | technical review | Continue Accepted ADR-001 Option A (`app/`); no `src/` migrate this INIT | resolved | Accepted ADR-001; `docs/specification/reports/Technical-Review-INIT-REALWORLD-003.md` |

## Draft check summary (D1–D12)

| Check | Status | Evidence / findings |
|-------|--------|---------------------|
| D1 Approved handoff current | PASS | H1 digest matches PRD file `sha256:5cccf070…`; H3 map_revision=1; H2 api scope digest `sha256:6e1a5775…`; G1 APPROVED review `commit_id` = meta PR #10 head `abfbbcff…`; label `impact-map-lgtm`; repo affected not deferred/blocked |
| D1b No open blocking IM-* | PASS | Impact-map §10: IM-01..IM-07 all `Blocking: no`; Gate 1 note allows defaults for spec-draft |
| D2 Complete PRD traceability | PASS | CAP-01..CAP-03 each have ≥1 REQ; every REQ cites PRD CAP/REQ or OQ/IM default |
| D2b Journeys carried | PASS | J-01..J-12 carried; live evidence cites CAP/J |
| D3 Repo-bounded scope | PASS | Provider scope matches impact-map H2; web/local deferred and non-goals listed under Out of scope |
| D4 Observable acceptance | PASS | Each REQ has condition/event, observable result, evidence layer; implementation-neutral |
| D5 Negative/failure paths | PASS | Table covers empty/blank, unseated, peer isolation, empty recall, missing identity, durability, immutability |
| D6 Assumptions/questions | PASS | Assumptions evidenced; questions have lane/owner/blocking/default/status; material PM defaults applied into REQs |
| D7 Cross-repository contracts | PASS | None — no cross-repo product seam (PRD §8; impact-map §6) |
| D8 NFR applicability | PASS | All eight areas specified or N/A with reason |
| D9 As-built alignment | PASS | As-built index absent; source scan: no park/saved-search surface under `app/` — CAP-01..CAP-03 are new; seat/auth baseline from INIT-001 remains |
| D10 Dependency order | PASS | Matches impact-map: sole build order `drivestream-lab/realworld-api`; api depends on none |
| D11 Zero unresolved blockers | PASS | No blocking Q remaining; Q-08 non-blocking PE architecture question for TDD |
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
| Proposed branch | `chore/INIT-REALWORLD-003-spec-realworld-api` |
| Proposed base | `develop` |
| Proposed title | `[INIT-REALWORLD-003] Spec — realworld-api` |
| PR type | **Draft** (entire spec lifecycle) |
| Local artifacts to publish | `docs/specification/product/INIT-REALWORLD-003-api.md`, `docs/specification/README.md` |
| Forge readiness | fill `handoff.forge` for `open_draft_pr`; recommend `/commit-workspace` then `/open-draft-pr` — do not commit/push/open PR inside this skill |
| Reviewer | @drivestream-lab/backend-devs |
| Initial Gate 2 label | `spec-pending` |
| Additional invalidation label | none |
| Blocking items | none |

**No GitHub side effects have occurred.** Persist the draft locally; Forge publish is a later `/commit-workspace` / `/open-draft-pr` or Gateflow ForgeClient step.

### Proposed Draft PR body

```markdown
## Initiative

INIT-REALWORLD-003 — Replay-ready personal search memory

## Meta handoff

- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/10
- Approved meta head: `abfbbcff877a83c298776fd4801b8ac4c75ddfba`
- Impact-map revision: 1
- PRD digest: `sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8`
- Repo scope digest: `sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7`

## Spec path

`docs/specification/product/INIT-REALWORLD-003-api.md`

## Summary

- 16 REQs covering CAP-01..CAP-03 as API provider (no cross-repo CTR this INIT)
- Park / recall / relabel / discard with query fidelity, durability, and peer/unseated isolation; web/local out of scope
- Q-08 chassis resolved: continue Accepted ADR-001 (`app/`); see Technical-Review-INIT-REALWORLD-003

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

- PRD: `realworld-meta/prd/INIT-REALWORLD-003.md`
- Meta PRD PR: https://github.com/drivestream-lab/realworld-meta/pull/10
- Spec PR: pending
- Service profile: not present (`docs/specification/product/00-service-profile.md` absent)

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: spec-draft
  outcome: pass
  artifact:
    path: docs/specification/product/INIT-REALWORLD-003-api.md
  blockers: []
  signals:
    pr_ready: true
    draft_verdict: PASS
    map_revision: 1
    meta_pr: https://github.com/drivestream-lab/realworld-meta/pull/10
    meta_pr_approved_head: abfbbcff877a83c298776fd4801b8ac4c75ddfba
    prd_digest: sha256:5cccf07066a0333027279aac0cae64d3f3be10773b7a5b37106302f2bbb9ceb8
    scope_digest: sha256:6e1a5775a890e03ad0295e43e795e36962fd431132a03412cf647282dc8331c7
    open_non_blocking_questions: []
  next_candidates:
    - spec-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels:
      - spec-pending
    title: "[INIT-REALWORLD-003] Spec — realworld-api"
    body_path: docs/specification/product/INIT-REALWORLD-003-api.md
```
