.PHONY: verify check

# Overlay. Runtime verify is host HTTP against realworld-local compose.
verify:
	curl -sf http://localhost:3100/api/articles >/dev/null
	@echo "api articles: ok"

# Incremental W0 static check (ADR-001): black only — not full pyright/import-linter.
check:
	.venv/bin/poetry run black --check app tests
