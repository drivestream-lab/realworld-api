# prayog:covers: CAP-01, CAP-02, J-01, J-05, J-07, J-08, J-11, J-17, REQ-01, REQ-08, REQ-10, REQ-12, REQ-34
"""Live smoke for INIT-REALWORLD-001 W0 — seat + public bulletin.

Human-run against realworld-local compose (default http://localhost:3100).
Does not replace unit tests. Exit 0 only when scriptable probes pass; look-ats
are printed for wave-acceptance (newest-first feed; deny publish after bearer omit).
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
DEFAULT_BASE_URL = "http://localhost:3100"


def _base_url() -> str:
    return os.environ.get("REALWORLD_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _request(
    method: str,
    path: str,
    *,
    body: dict[str, Any] | None = None,
    token: str | None = None,
) -> tuple[int, dict[str, Any] | list[Any] | None]:
    url = f"{_base_url()}{path}"
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Token {token}"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            payload: dict[str, Any] | list[Any] | None
            payload = json.loads(raw) if raw else None
            return int(resp.status), payload
    except HTTPError as exc:
        raw = exc.read().decode("utf-8")
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = None
        return int(exc.code), payload
    except URLError as exc:
        raise SystemExit(f"[ERROR] API unreachable at {_base_url()}: {exc}") from exc


def _pass(label: str) -> None:
    print(f"[OK] PASS {label}")


def _fail(label: str, detail: str) -> None:
    print(f"[ERROR] FAIL {label}: {detail}")
    raise SystemExit(1)


def verify_cap01_bulletin() -> None:
    stimulus = _load_json(FIXTURES_ROOT / "cap-01-bulletin" / "stimulus.json")
    expected = _load_json(FIXTURES_ROOT / "cap-01-bulletin" / "expected.json")

    status, payload = _request("GET", stimulus["list_path"])
    if status != expected["list_status"]:
        _fail("CAP-01 list", f"status={status}")
    if not isinstance(payload, dict) or "articles" not in payload:
        _fail("CAP-01 list", "missing articles key")
    _pass("CAP-01 guest global feed (REQ-01 / J-01)")

    articles = payload.get("articles") or []
    if articles:
        slug = articles[0]["slug"]
        status, article_payload = _request("GET", f"/api/articles/{slug}")
        if status != expected["get_status"]:
            _fail("CAP-01 get", f"status={status}")
        if not isinstance(article_payload, dict) or "article" not in article_payload:
            _fail("CAP-01 get", "missing article key")
        _pass("CAP-01 guest open article (REQ-02)")
    else:
        _pass("CAP-01 empty bulletin allowed (REQ-01 empty set)")


def verify_cap02_seat() -> None:
    stimulus = _load_json(FIXTURES_ROOT / "cap-02-seat" / "stimulus.json")
    expected = _load_json(FIXTURES_ROOT / "cap-02-seat" / "expected.json")
    suffix = uuid.uuid4().hex[:10]
    user = {
        "username": f"{stimulus['username_prefix']}{suffix}",
        "email": f"{stimulus['email_prefix']}{suffix}@example.com",
        "password": stimulus["password"],
    }

    status, reg = _request("POST", "/api/users", body={"user": user})
    if status != expected["register_status"]:
        _fail("CAP-02 register", f"status={status}")
    if not isinstance(reg, dict) or "user" not in reg:
        _fail("CAP-02 register", "missing user")
    token = reg["user"].get("token") or ""
    if token:
        _fail("CAP-02 register", "register must not issue a usable seat token (REQ-08)")
    _pass("CAP-02 register eligibility without seat (REQ-08 / J-05)")

    status, login = _request(
        "POST",
        "/api/users/login",
        body={"user": {"email": user["email"], "password": user["password"]}},
    )
    if status != expected["login_status"]:
        _fail("CAP-02 login", f"status={status}")
    if not isinstance(login, dict) or not (login.get("user") or {}).get("token"):
        _fail("CAP-02 login", "missing seat token (REQ-10)")
    seat = login["user"]["token"]
    _pass("CAP-02 login seats (REQ-10 / J-05)")

    status, _ = _request(
        "POST",
        "/api/articles",
        body={
            "article": {
                "title": f"w0-deny-{suffix}",
                "description": "unseated",
                "body": "unseated",
                "tagList": ["w0"],
            }
        },
    )
    if status not in expected["unseated_create_statuses"]:
        _fail("CAP-02 unseated create", f"status={status} (expected deny)")
    _pass("CAP-02 unseated mutate denied (REQ-12 / REQ-14 / J-08)")

    # Prove seat still works when bearer present (sanity; not a look-at).
    status, created = _request(
        "POST",
        "/api/articles",
        body={
            "article": {
                "title": f"w0-seat-{suffix}",
                "description": "seated",
                "body": "seated",
                "tagList": ["w0"],
            }
        },
        token=seat,
    )
    if status not in (200, 201):
        _fail("CAP-02 seated create sanity", f"status={status}")
    if isinstance(created, dict) and created.get("article", {}).get("slug"):
        _pass("CAP-02 reseat path usable after login (REQ-13)")
    else:
        _fail("CAP-02 seated create sanity", "missing slug")


def print_human_lookats() -> None:
    print("")
    print("[INFO] Human look-ats (wave-acceptance — not auto-claimed):")
    print(
        "  1) GET /api/articles with ≥2 articles → newest-first by updated_at/created_at"
    )
    print(
        "  2) POST /api/articles without Authorization → deny (401/403); no article created"
    )
    print("  Ack accept with GitHub label wave-accepted on the tip.")


def main() -> None:
    print(f"[INFO] verify_wave0_seat_bulletin against {_base_url()}")
    verify_cap01_bulletin()
    verify_cap02_seat()
    print_human_lookats()
    print(
        "[OK] Scriptable W0 probes passed; complete human look-ats before wave-accepted"
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
