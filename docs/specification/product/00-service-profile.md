# Service profile — realworld-api

| Field | Value |
|-------|-------|
| Repo | `drivestream-lab/realworld-api` |
| Role | HTTP API **provider** for RealWorld Conduit-shaped bulletin + contribution seat |
| Profile | Internal consumer only for sibling S2S — **no** inbound `/internal/v1` required for INIT-REALWORLD-001; public Conduit-style API is the product surface |
| Consumers | `realworld-web` (UAT surface); `realworld-local` (compose prove) |
| Source layout (as-found) | Legacy Conduit FastAPI tree under `app/` (routes, services, repositories, models) — chassis migration to `src/` is **not** decided in product specs |

## Domain this repo owns

- Public bulletin reads (global listing, tag filter, article open, public profile + author articles)
- Contribution seat lifecycle (register eligibility, authenticate seat, unseat, reseat)
- Seated publish / own-article revise-delete with ≥1 tag
- Private favorites shelf (isolated; no public who-favorited social proof)
- Own nameplate self-update (editable public fields)

## Explicit non-ownership (other repos / non-goals)

- Web UAT chrome and kill-path driving — `realworld-web`
- Compose / local prove environment — `realworld-local`
- Comments, follow graphs, personalized feeds, OAuth, email verification, admin tooling — out of INIT-REALWORLD-001
