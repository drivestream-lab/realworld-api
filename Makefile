.PHONY: verify check

# Overlay. Runtime verify is host HTTP against realworld-local compose.
verify:
	curl -sf http://localhost:3100/api/articles >/dev/null
	@echo "api articles: ok"

# Incremental static check (ADR-001 / W0): black --check on app + tests.
check:
	poetry run black --check app tests
