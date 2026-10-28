.PHONY: verify

# Overlay. Runtime verify is host HTTP against realworld-local compose.
verify:
	curl -sf http://localhost:3100/api/articles >/dev/null
	@echo "api articles: ok"
