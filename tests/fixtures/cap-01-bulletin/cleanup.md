# Cleanup — cap-01-bulletin

No synthetic rows are written by the CAP-01 guest-read probes.

If a human seeded articles for look-ats, delete those slugs via seated author
`DELETE /api/articles/{slug}` or SQL against the local compose database.
