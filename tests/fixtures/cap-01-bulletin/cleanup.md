# Cleanup — cap-01-bulletin

Safe test data only (synthetic W0 users/articles created by `verify_wave0_seat_bulletin`).

1. Delete articles whose titles start with `W0 Bulletin` for the synthetic author created in the run.
2. Optionally delete the synthetic user created by the paired CAP-02 seat fixture (same username suffix).
3. Do not touch non-synthetic production-like rows.
