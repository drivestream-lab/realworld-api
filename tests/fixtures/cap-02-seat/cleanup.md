# Cleanup — cap-02-seat

1. Remove synthetic users with username prefix `w0seat-`.
2. Remove articles authored by those users (titles `W0 Bulletin …`).
3. Client JWT discard is the unseat signal (ADR-004) — no server logout row to clear.
