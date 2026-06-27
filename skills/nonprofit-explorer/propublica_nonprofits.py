#!/usr/bin/env python3
"""ProPublica Nonprofit Explorer API client.

Wraps the public, **unauthenticated** Nonprofit Explorer API:

    https://projects.propublica.org/nonprofits/api

There is no API key and no auth header — every endpoint is an open GET.

Design goals (the agent must be able to die cleanly on any failure):
  * Standard library only — no pip install, nothing to vendor.
  * Every network call is bounded by a timeout; nothing can hang forever.
  * Transient failures (timeouts, 5xx, 429) get a few bounded retries with
    exponential backoff; permanent failures (4xx, bad JSON) fail fast.
  * A failure NEVER leaves a half-written result on stdout. On error we print
    a structured JSON object to STDERR and exit with a non-zero status, so a
    supervising agent can detect the failure and terminate safely.
  * SIGINT / SIGTERM are handled: an interrupted request exits 130 / 143
    promptly instead of leaving a zombie connection open.

Exit codes (CLI):
    0   success
    2   bad usage / invalid arguments
    3   API error (HTTP 4xx, bad JSON, validation)
    4   network error after retries (timeout, connection, 5xx, 429)
    130 interrupted (SIGINT / Ctrl-C)
    143 terminated (SIGTERM)
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

__all__ = ["search", "get_organization", "ApiError", "NetworkError"]

BASE_URL = "https://projects.propublica.org/nonprofits/api/v2"
USER_AGENT = "nonprofit-explorer-skill/1.0 (+https://projects.propublica.org/nonprofits/api)"

# Bounded so the agent can never hang on a stalled connection.
DEFAULT_CONNECT_TIMEOUT = 10.0   # seconds to establish the socket
DEFAULT_READ_TIMEOUT = 20.0      # seconds to read the response
DEFAULT_RETRIES = 3              # attempts for *transient* failures
DEFAULT_BACKOFF = 1.5            # base seconds; grows exponentially

# HTTP statuses worth retrying — everything else is treated as permanent.
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}

# Valid filter ranges per the API docs.
_VALID_NTEE = set(range(1, 11))                       # 1..10
_VALID_C_CODE = set(range(2, 29)) | {92}              # 501(c)(2..28) + 4947(a)(1)


class ApiError(Exception):
    """Permanent failure: bad request, 4xx, or malformed response.

    Retrying will not help, so we surface it immediately.
    """

    def __init__(self, message: str, *, status: int | None = None, url: str | None = None):
        super().__init__(message)
        self.status = status
        self.url = url


class NetworkError(Exception):
    """Transient failure that survived all retries (timeout/5xx/429/conn)."""

    def __init__(self, message: str, *, url: str | None = None, attempts: int = 0):
        super().__init__(message)
        self.url = url
        self.attempts = attempts


def _build_url(path: str, params: dict[str, Any] | None = None) -> str:
    """Join the base, a path, and percent-encoded query params."""
    url = f"{BASE_URL}/{path.lstrip('/')}"
    if params:
        # Drop None values; the API treats absent params as "no filter".
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url = f"{url}?{urllib.parse.urlencode(clean)}"
    return url


def _request_json(
    url: str,
    *,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    read_timeout: float = DEFAULT_READ_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    backoff: float = DEFAULT_BACKOFF,
) -> dict[str, Any]:
    """GET ``url`` and return parsed JSON, with bounded retries.

    Raises ``ApiError`` on permanent failure, ``NetworkError`` on transient
    failure that outlives every retry. Never hangs: every attempt is bounded
    by ``read_timeout`` (which urllib applies as an overall socket timeout).
    """
    # urllib uses a single timeout for the whole socket op; use the larger.
    timeout = max(connect_timeout, read_timeout)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")

    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, ValueError) as exc:
                # A 200 with non-JSON body is a permanent problem; don't retry.
                raise ApiError(f"Response was not valid JSON: {exc}", url=url) from exc

        except urllib.error.HTTPError as exc:
            status = exc.code
            if status in _RETRYABLE_STATUS and attempt < retries:
                last_exc = exc
                _sleep_backoff(exc, attempt, backoff)
                continue
            if status in _RETRYABLE_STATUS:
                raise NetworkError(
                    f"HTTP {status} after {attempt} attempt(s)", url=url, attempts=attempt
                ) from exc
            # 4xx (e.g. 404 unknown EIN, 400 bad param) — permanent.
            raise ApiError(f"HTTP {status} {exc.reason}", status=status, url=url) from exc

        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            # DNS failure, connection refused, timeout, reset — transient.
            last_exc = exc
            if attempt < retries:
                _sleep_backoff(None, attempt, backoff)
                continue
            raise NetworkError(
                f"Network failure after {attempt} attempt(s): {exc}", url=url, attempts=attempt
            ) from exc

    # Unreachable, but keeps type-checkers and the logic honest.
    raise NetworkError(f"Exhausted retries: {last_exc}", url=url, attempts=retries)


def _sleep_backoff(exc: Exception | None, attempt: int, base: float) -> None:
    """Sleep before a retry, honoring Retry-After when the server sends it."""
    delay = base * (2 ** (attempt - 1))
    retry_after = getattr(exc, "headers", None)
    if retry_after is not None:
        hdr = retry_after.get("Retry-After")
        if hdr and hdr.isdigit():
            delay = max(delay, float(hdr))
    time.sleep(delay)


def search(
    q: str | None = None,
    *,
    page: int = 0,
    state: str | None = None,
    ntee: int | None = None,
    c_code: int | None = None,
    **request_kwargs: Any,
) -> dict[str, Any]:
    """Search nonprofits. Mirrors GET /search.json.

    Args:
        q: Keyword query (org name, alt name, city). Supports the API's
           +require / -exclude / "exact phrase" operators.
        page: Zero-indexed page number (25 results per page).
        state: Two-letter USPS state code (e.g. "NY"); "ZZ" for foreign filers.
        ntee: NTEE major group, 1-10.
        c_code: 501(c) subsection (2-28) or 92 for 4947(a)(1).
        request_kwargs: Forwarded to the HTTP layer (timeouts, retries).

    Returns the parsed JSON dict ({"organizations": [...], ...}).
    Raises ApiError / NetworkError on failure.
    """
    if state is not None:
        state = state.strip().upper()
        if len(state) != 2 or not state.isalpha():
            raise ApiError(f"state must be a 2-letter code, got {state!r}")
    if ntee is not None and ntee not in _VALID_NTEE:
        raise ApiError(f"ntee must be 1-10, got {ntee!r}")
    if c_code is not None and c_code not in _VALID_C_CODE:
        raise ApiError(f"c_code must be 2-28 or 92, got {c_code!r}")
    if page < 0:
        raise ApiError(f"page must be >= 0, got {page!r}")

    params: dict[str, Any] = {"page": page}
    if q:
        params["q"] = q
    if state is not None:
        params["state[id]"] = state
    if ntee is not None:
        params["ntee[id]"] = ntee
    if c_code is not None:
        params["c_code[id]"] = c_code

    return _request_json(_build_url("search.json", params), **request_kwargs)


def get_organization(ein: str | int, **request_kwargs: Any) -> dict[str, Any]:
    """Fetch one organization and its filings. Mirrors GET /organizations/:ein.json.

    Args:
        ein: Employer Identification Number. Accepts "14-2007220", "142007220",
             or an int; non-digits are stripped.
        request_kwargs: Forwarded to the HTTP layer (timeouts, retries).

    Returns the parsed JSON dict. Raises ApiError (e.g. 404 for unknown EIN) /
    NetworkError on failure.
    """
    digits = "".join(ch for ch in str(ein) if ch.isdigit())
    if not digits:
        raise ApiError(f"EIN must contain digits, got {ein!r}")
    return _request_json(_build_url(f"organizations/{digits}.json"), **request_kwargs)


# ---------------------------------------------------------------------------
# CLI — structured stdout on success, structured stderr + exit code on failure.
# ---------------------------------------------------------------------------
def _install_signal_handlers() -> None:
    """Exit promptly and with conventional codes on SIGINT / SIGTERM.

    This is what lets a supervising agent *kill the process safely*: the
    handler raises KeyboardInterrupt / SystemExit so any open socket is torn
    down by normal stack unwinding rather than abandoned.
    """
    def _term(signum, _frame):  # pragma: no cover - signal path
        # 128 + signal number is the POSIX convention.
        sys.exit(128 + signum)

    # SIGINT already raises KeyboardInterrupt; only override SIGTERM.
    try:
        signal.signal(signal.SIGTERM, _term)
    except (ValueError, OSError):
        # Not on the main thread (e.g. imported by a host) — skip silently.
        pass


def _fail(kind: str, exc: Exception, code: int) -> int:
    """Emit a structured error to stderr and return the exit code."""
    payload = {
        "ok": False,
        "error": kind,
        "message": str(exc),
        "status": getattr(exc, "status", None),
        "url": getattr(exc, "url", None),
    }
    print(json.dumps(payload), file=sys.stderr)
    return code


def main(argv: list[str] | None = None) -> int:
    _install_signal_handlers()

    parser = argparse.ArgumentParser(
        prog="propublica_nonprofits",
        description="Query the ProPublica Nonprofit Explorer API (no key required).",
    )
    parser.add_argument("--connect-timeout", type=float, default=DEFAULT_CONNECT_TIMEOUT)
    parser.add_argument("--read-timeout", type=float, default=DEFAULT_READ_TIMEOUT)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")

    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search organizations.")
    p_search.add_argument("query", nargs="?", default=None, help="Keyword query.")
    p_search.add_argument("--page", type=int, default=0)
    p_search.add_argument("--state", default=None, help="Two-letter state code.")
    p_search.add_argument("--ntee", type=int, default=None, help="NTEE group 1-10.")
    p_search.add_argument("--c-code", type=int, default=None, dest="c_code")

    p_org = sub.add_parser("org", help="Fetch one organization by EIN.")
    p_org.add_argument("ein", help="EIN, e.g. 14-2007220 or 142007220.")

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse exits 2 on bad usage; preserve that.
        return int(exc.code) if exc.code is not None else 2

    http_kwargs = {
        "connect_timeout": args.connect_timeout,
        "read_timeout": args.read_timeout,
        "retries": args.retries,
    }

    try:
        if args.command == "search":
            result = search(
                args.query,
                page=args.page,
                state=args.state,
                ntee=args.ntee,
                c_code=args.c_code,
                **http_kwargs,
            )
        elif args.command == "org":
            result = get_organization(args.ein, **http_kwargs)
        else:  # pragma: no cover - argparse enforces this
            parser.error(f"unknown command {args.command!r}")
            return 2
    except ApiError as exc:
        return _fail("api_error", exc, 3)
    except NetworkError as exc:
        return _fail("network_error", exc, 4)
    except KeyboardInterrupt:
        print(json.dumps({"ok": False, "error": "interrupted"}), file=sys.stderr)
        return 130

    print(json.dumps(result, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        # Last-resort guard so Ctrl-C never dumps a traceback.
        sys.exit(130)
