"""HTTP client tool for the Congress.gov REST API."""

import json

import requests

from .config import CONGRESS_API_BASE, CONGRESS_API_KEY


def congress_fetch(path: str, params_json: str = "{}") -> dict:
    """Fetch JSON from the Congress.gov API.

    Args:
        path: API path beginning with '/', exactly as documented in a skill,
            e.g. '/bill', '/bill/117/hr/3076', or '/member/L000174'.
        params_json: A JSON object string of query parameters, e.g.
            '{"limit": "5", "fromDateTime": "2023-01-01T00:00:00Z"}'.
            Pass '{}' if there are none. Do NOT include api_key or format.

    Returns:
        The parsed JSON response, or {"error": "..."} on failure.
    """
    if not CONGRESS_API_KEY:
        return {"error": "CONGRESS_API_KEY is not set. Get one at https://api.congress.gov/sign-up/"}

    try:
        params = json.loads(params_json) if params_json else {}
    except json.JSONDecodeError as exc:
        return {"error": f"params_json is not valid JSON: {exc}"}

    params = {k: str(v) for k, v in params.items()}
    params.setdefault("format", "json")
    params["api_key"] = CONGRESS_API_KEY

    url = f"{CONGRESS_API_BASE}/{path.lstrip('/')}"
    try:
        response = requests.get(url, params=params, timeout=30)
    except requests.RequestException as exc:
        return {"error": f"request failed: {exc}", "path": path}

    if response.status_code != 200:
        return {
            "error": f"HTTP {response.status_code}",
            "path": path,
            "detail": response.text[:500],
        }

    try:
        return response.json()
    except ValueError:
        return {"error": "response was not JSON", "path": path, "detail": response.text[:500]}
