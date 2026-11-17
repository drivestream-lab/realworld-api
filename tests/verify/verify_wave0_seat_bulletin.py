"""W0 live verify — seat lifecycle + public bulletin.

prayog:covers: CAP-01, CAP-02, J-01, J-05, J-07, J-08, J-11, J-17, REQ-01, REQ-08, REQ-10, REQ-12, REQ-34

Human-run against realworld-local compose (API on :3100). This module is
co-shipped by TASK-W0-04; /loop-spec does not claim smoke success.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
DEFAULT_BASE_URL = "http://localhost:3100"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _request(
    method: str,
    url: str,
    *,
    body: dict[str, Any] | None = None,
    token: str | None = None,
) -> tuple[int, dict[str, Any] | list[Any] | None]:
    data = None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Token {token}"
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            payload: dict[str, Any] | list[Any] | None
            payload = json.loads(raw) if raw else None
            return resp.status, payload
    except HTTPError as exc:
        raw = exc.read().decode("utf-8")
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = None
        return exc.code, payload


def _fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def _pass(message: str) -> None:
    print(f"[PASS] {message}")


def main() -> int:
    base_url = DEFAULT_BASE_URL.rstrip("/")
    cap01 = _load_json(FIXTURES_ROOT / "cap-01-bulletin" / "stimulus.json")
    cap02 = _load_json(FIXTURES_ROOT / "cap-02-seat" / "stimulus.json")
    expected_cap01 = _load_json(FIXTURES_ROOT / "cap-01-bulletin" / "expected.json")
    expected_cap02 = _load_json(FIXTURES_ROOT / "cap-02-seat" / "expected.json")

    # Preflight
    try:
        status, _ = _request("GET", f"{base_url}{cap01['paths']['list_articles']}")
    except URLError as exc:
        _fail(f"API unreachable at {base_url}: {exc}")
    if status != 200:
        _fail(f"guest list preflight expected 200, got {status}")

    suffix = uuid.uuid4().hex[:10]
    username = f"{cap02['register']['username_prefix']}-{suffix}"
    email = f"{cap02['register']['email_local']}+{suffix}@{cap02['register']['email_domain']}"
    password = cap02["register"]["password"]

    # CAP-02 / J-05 — register without seat
    status, body = _request(
        "POST",
        f"{base_url}{cap02['paths']['register']}",
        body={"user": {"username": username, "email": email, "password": password}},
    )
    if status != expected_cap02["register_status"]:
        _fail(f"register status {status} != {expected_cap02['register_status']}")
    if not isinstance(body, dict) or body.get("user", {}).get("token"):
        _fail("register must not mint a usable seat token")
    _pass("CAP-02 register eligibility without seat token")

    # Duplicate register fail-closed
    status, _ = _request(
        "POST",
        f"{base_url}{cap02['paths']['register']}",
        body={"user": {"username": username, "email": email, "password": password}},
    )
    if status != expected_cap02["duplicate_register_status"]:
        _fail(f"duplicate register status {status}")
    _pass("CAP-02 duplicate register fail-closed")

    # Invalid login
    status, _ = _request(
        "POST",
        f"{base_url}{cap02['paths']['login']}",
        body={"user": {"email": email, "password": "wrong-password"}},
    )
    if status != expected_cap02["invalid_login_status"]:
        _fail(f"invalid login status {status}")
    _pass("CAP-02 / J-11 invalid login refuse")

    # Login seats
    status, body = _request(
        "POST",
        f"{base_url}{cap02['paths']['login']}",
        body={"user": {"email": email, "password": password}},
    )
    if status != expected_cap02["login_status"]:
        _fail(f"login status {status}")
    if not isinstance(body, dict):
        _fail("login response not JSON object")
    token = body.get("user", {}).get("token")
    if not token:
        _fail("login must return seat token")
    _pass("CAP-02 / J-05 login seats")

    # Seated publish (stimulus for bulletin ordering + guest open)
    article_title = f"{cap01['publish']['title_prefix']} {suffix}"
    status, body = _request(
        "POST",
        f"{base_url}{cap01['paths']['create_article']}",
        body={
            "article": {
                "title": article_title,
                "description": cap01["publish"]["description"],
                "body": cap01["publish"]["body"],
                "tagList": cap01["publish"]["tagList"],
            }
        },
        token=token,
    )
    if status not in (200, 201):
        _fail(f"seated publish status {status}")
    if not isinstance(body, dict):
        _fail("publish response not JSON object")
    slug = body.get("article", {}).get("slug")
    if not slug:
        _fail("publish missing slug")
    _pass("stimulus publish for CAP-01 bulletin")

    # Second article for ordering
    status, body2 = _request(
        "POST",
        f"{base_url}{cap01['paths']['create_article']}",
        body={
            "article": {
                "title": f"{article_title} later",
                "description": cap01["publish"]["description"],
                "body": cap01["publish"]["body"],
                "tagList": cap01["publish"]["tagList"],
            }
        },
        token=token,
    )
    if status not in (200, 201) or not isinstance(body2, dict):
        _fail(f"second publish failed status={status}")
    slug2 = body2.get("article", {}).get("slug")

    # Unseat via client JWT discard (ADR-004) — omit Authorization
    status, _ = _request(
        "POST",
        f"{base_url}{cap01['paths']['create_article']}",
        body={
            "article": {
                "title": "should-deny",
                "description": "x",
                "body": "x",
                "tagList": ["x"],
            }
        },
    )
    if status not in expected_cap02["unseated_mutate_status"]:
        _fail(
            f"unseated mutate status {status} not in {expected_cap02['unseated_mutate_status']}"
        )
    _pass("CAP-02 / J-08 unseated contribution denied")

    # CAP-01 guest bulletin reads
    status, listed = _request("GET", f"{base_url}{cap01['paths']['list_articles']}")
    if status != expected_cap01["list_status"]:
        _fail(f"guest list status {status}")
    if not isinstance(listed, dict):
        _fail("guest list not object")
    articles = listed.get("articles") or []
    slugs = [a.get("slug") for a in articles]
    if slug not in slugs or slug2 not in slugs:
        _fail("published slugs missing from guest feed")
    if slugs.index(slug2) > slugs.index(slug):
        # newer (slug2) should appear before older (slug) when created later
        _fail("feed not newest-first (REQ-34)")
    _pass("CAP-01 / J-01 guest feed newest-first")

    status, opened = _request(
        "GET", f"{base_url}{cap01['paths']['get_article']}/{slug2}"
    )
    if status != expected_cap01["get_status"]:
        _fail(f"guest open status {status}")
    if not isinstance(opened, dict) or opened.get("article", {}).get("slug") != slug2:
        _fail("guest open article mismatch")
    _pass("CAP-01 guest open article")

    tag = cap01["publish"]["tagList"][0]
    status, tagged = _request(
        "GET", f"{base_url}{cap01['paths']['list_articles']}?tag={tag}"
    )
    if status != 200 or not isinstance(tagged, dict):
        _fail(f"guest tag lane failed status={status}")
    _pass("CAP-01 / J-02 guest tag lane")

    status, profile = _request(
        "GET", f"{base_url}{cap01['paths']['get_profile']}/{username}"
    )
    if status != 200 or not isinstance(profile, dict):
        _fail(f"guest profile failed status={status}")
    _pass("CAP-01 / J-03 guest public profile")

    print("[OK] verify_wave0_seat_bulletin complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
