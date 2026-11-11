# Implementation status (as-built index)

> Bootstrap index written during `/spec-draft` for INIT-REALWORLD-001 because no prior
> `docs/specification/` tree existed. Rows describe **current tree evidence** under
> `app/`, not Wave0a acceptance.

| Capability / surface | Status | Evidence | Notes |
|----------------------|--------|----------|-------|
| Public article list / get / tag filter | present (legacy) | `app/api/routes/articles/` | Ungated list/get exist; empty states allowed by Conduit shape |
| Public profiles | present (legacy) | `app/api/routes/profiles.py` | Follow endpoints exist (out of INIT scope) |
| Register / login | present (legacy) | `app/api/routes/authentication.py` | Register returns JWT (`UserWithToken`) — conflicts with OQ-04 Wave0a default (eligibility then login for kill path) |
| Current-user get/update | present (legacy) | `app/api/routes/users.py`, `app/models/schemas/users.py` | `UserInUpdate` allows username/email — OQ-03 locks those for Wave0a |
| Article create/update/delete | present (legacy) | `app/api/routes/articles/articles_resource.py`, `app/models/schemas/articles.py` | `ArticleInCreate.tagList` defaults to `[]`; `ArticleInUpdate` omits tags — gaps vs REQ-16/21/22 |
| Favorites | present (legacy) | `app/api/routes/articles/articles_common.py` | No own-article favorite refusal; response updates `favorites_count` (social-proof non-goal) |
| Personalized feed | present (legacy) | `GET /articles/feed` | **Out of scope** for INIT-REALWORLD-001 |
| Comments | present (legacy) | `app/api/routes/comments.py` | **Out of scope** |
| Tags list | present (legacy) | `app/api/routes/tags.py` | Supporting discovery; not a separate CAP |
| Spec slice INIT-REALWORLD-001 | draft | `docs/specification/product/INIT-REALWORLD-001-api.md` | Not implemented / not live-verified |
| Chassis `src/` layout | absent | tree | Harness overlays present; product code still under `app/` |

Per-initiative detail: none yet (`Implementation-Status-INIT-REALWORLD-001.md` after waves).
