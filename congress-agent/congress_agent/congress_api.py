"""HTTP client tool for the government REST APIs (Congress.gov and OpenFEC).

A single ``api_fetch`` routes to the right API based on a skill's ``source``
(``congress`` or ``fec``), so one researcher can fetch from either. Auth and base
URL per source come from ``config.SOURCES``; both APIs authenticate with an
``api_key`` query parameter.
"""

import json

import requests

from .config import SOURCES


def api_fetch(source: str, path: str, params_json: str = "{}") -> dict:
    """Fetch JSON from a government API (Congress.gov or OpenFEC).

    Args:
        source: Which API to hit — 'congress' (Congress.gov) or 'fec' (OpenFEC).
            This is the prefix of the skill name, e.g. for skill 'fec/candidate'
            the source is 'fec'.
        path: API path beginning with '/', exactly as documented in the skill's
            reference (relative to that API's base URL), e.g. '/bill/117/hr/3076'
            for congress or '/candidate/P00009423/' for fec.
        params_json: A JSON object string of query parameters, e.g.
            '{"limit": "5"}' (congress) or '{"cycle": "2024"}' (fec). Pass '{}' if
            there are none. Do NOT include api_key or format.

    Returns:
        The parsed JSON response, or {"error": "..."} on failure.
    """
    cfg = SOURCES.get(source)
    if cfg is None:
        return {"error": f"unknown source '{source}'. Valid sources: {', '.join(SOURCES)}"}
    if not cfg["api_key"]:
        return {"error": f"API key for source '{source}' is not set."}

    try:
        params = json.loads(params_json) if params_json else {}
    except json.JSONDecodeError as exc:
        return {"error": f"params_json is not valid JSON: {exc}"}

    params = {k: str(v) for k, v in params.items()}
    for key, value in cfg["extra_params"].items():
        params.setdefault(key, value)
    params["api_key"] = cfg["api_key"]

    url = f"{cfg['base']}/{path.lstrip('/')}"
    try:
        response = requests.get(url, params=params, timeout=30)
    except requests.RequestException as exc:
        return {"error": f"request failed: {exc}", "source": source, "path": path}

    if response.status_code != 200:
        return {
            "error": f"HTTP {response.status_code}",
            "source": source,
            "path": path,
            "detail": response.text[:500],
        }

    try:
        return response.json()
    except ValueError:
        return {"error": "response was not JSON", "source": source, "path": path,
                "detail": response.text[:500]}
