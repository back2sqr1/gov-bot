---
name: nonprofit-explorer
description: Query the ProPublica Nonprofit Explorer API for U.S. nonprofit/tax-exempt organization data (IRS Form 990 filings). Use when the user asks about a nonprofit's finances, EIN, revenue/expenses/assets, 990 filings, or wants to search tax-exempt organizations by name, state, NTEE category, or 501(c) subsection. The API is free and requires NO API key or authentication.
---

# Nonprofit Explorer

Wraps the **public, unauthenticated** [ProPublica Nonprofit Explorer API](https://projects.propublica.org/nonprofits/api). It exposes IRS data on ~1.8M tax-exempt organizations, including extracted Form 990 financials.

**There is no API key.** Every endpoint is an open `GET`. Do not look for or ask the user for credentials.

## When to use

- "How much revenue did <nonprofit> report?" / "Look up <org>'s 990."
- "Find 501(c)(3) environmental nonprofits in California."
- "What's the EIN for <org>?" / "Show me <org>'s recent filings."

## How to run

The skill ships a zero-dependency Python CLI (stdlib only — no `pip install`). Run it with the repo's Python 3.

Search organizations:

```bash
python3 skills/nonprofit-explorer/propublica_nonprofits.py search "propublica" --pretty
python3 skills/nonprofit-explorer/propublica_nonprofits.py search "wildlife" --state CA --ntee 3 --c-code 3
```

Fetch one organization (and its filings) by EIN:

```bash
python3 skills/nonprofit-explorer/propublica_nonprofits.py org 14-2007220 --pretty
```

### Search options

| Flag        | Meaning                                                              |
|-------------|----------------------------------------------------------------------|
| `query`     | Keyword (name/alt-name/city). Supports `+require`, `-exclude`, `"exact phrase"`. |
| `--page`    | Zero-indexed page (25 results/page).                                 |
| `--state`   | Two-letter USPS code (`NY`); `ZZ` for foreign filers.                |
| `--ntee`    | NTEE major group `1`–`10` (1=Arts, 3=Environment/Animals, 4=Health…).|
| `--c-code`  | 501(c) subsection `2`–`28`, or `92` for 4947(a)(1). `3` = 501(c)(3). |

Global flags: `--read-timeout`, `--connect-timeout`, `--retries`, `--pretty`.

## Output & failure contract

**This is built so the agent can be killed safely on any API failure.**

- **Success:** parsed JSON is printed to **stdout**; exit code `0`.
- **Failure:** a structured JSON error (`{"ok": false, "error": ..., "message": ..., "status": ..., "url": ...}`) is printed to **stderr**, nothing is written to stdout, and the process exits non-zero. Check the exit code before trusting stdout.

| Exit code | Meaning                                              |
|-----------|------------------------------------------------------|
| `0`       | Success                                              |
| `2`       | Bad usage / invalid arguments                        |
| `3`       | API error — HTTP 4xx (e.g. unknown EIN → 404), bad JSON, validation |
| `4`       | Network error after retries (timeout, 5xx, 429, conn)|
| `130`     | Interrupted (SIGINT / Ctrl-C)                        |
| `143`     | Terminated (SIGTERM)                                 |

Safety properties:
- Every request is **timeout-bounded** (`--connect-timeout`, `--read-timeout`) — it cannot hang forever.
- **Transient** failures (timeout, 5xx, 429) retry with exponential backoff and honor `Retry-After`; **permanent** failures (4xx, bad JSON) fail fast without retrying.
- `SIGINT`/`SIGTERM` unwind the stack and close the socket, exiting `130`/`143` — so a supervising agent can terminate it cleanly mid-request.

## Importable API

The CLI is also a library:

```python
from skills.nonprofit_explorer.propublica_nonprofits import (
    search, get_organization, ApiError, NetworkError,
)

try:
    hits = search("propublica", state="NY")
    org = get_organization("14-2007220")
except ApiError:      # permanent — surface to the user, don't retry
    ...
except NetworkError:  # transient — already retried; safe to abort/kill
    ...
```

## Etiquette

The JSON endpoints have no published rate limit, but be a good citizen: cache results and don't hammer. The `download-filing` PDF links **are** rate-limited. Usage implies agreement to ProPublica's Data Terms of Use.
