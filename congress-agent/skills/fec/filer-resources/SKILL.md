---
name: filer-resources
description: Useful tools for those who file with the FEC.
---

# Filer Resources API

Useful tools for those who file with the FEC. Look up RAD analyst with telephone extension by committee_id.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /rad-analyst/
Use this endpoint to look up the RAD Analyst for a committee. The mission of the Reports Analysis Division (RAD) is to ensure that campaigns and political committees file timely and accurate reports that fully disclose their financial activities. RAD is responsible for reviewing statements and financial reports filed by political committees participating in federal elections, providing assistance…

**Query parameters:**
- `analyst_id` (array<integer>): ID of RAD analyst
- `analyst_short_id` (array<integer>): Short ID of RAD analyst
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `email` (array<string>): Email of RAD analyst
- `max_assignment_update_date` (string): Filter results for assignment updates made before this date
- `min_assignment_update_date` (string): Filter results for assignment updates made after this date
- `name` (array<string>): Name of RAD analyst
- `telephone_ext` (array<integer>): Telephone extension of RAD analyst
- `title` (array<string>): Title of RAD analyst

### GET /state-election-office/
State laws and procedures govern elections for state or local offices as well as how candidates appear on election ballots. Contact the appropriate state election office for more information.

**Query parameters:**
- `state` (string, required): Enter a state (Ex: AK, TX, VA etc..) to find the local election offices contact information.
