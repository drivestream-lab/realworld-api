# Cleanup — cap-02-seat

The verify driver creates a synthetic user (`w0seat*` / `w0seat*@example.com`)
and may create a seated article (`w0-seat-*` slug).

Cleanup options on local compose:

1. Seated `DELETE /api/articles/{slug}` for the created article, then remove the
   user row from Postgres (`users` / related favorites).
2. Or reset the local database volume used by realworld-local.

Do not run against shared non-dev data.
