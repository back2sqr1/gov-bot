---
name: presidential
description: Data supporting fec.gov's presidential map.
---

# Presidential API

Data supporting fec.gov's presidential map. For more information about the presidential map data available to download from fec.gov, please visit: https://www.fec.gov/campaign-finance-data/presidential-map-data/

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /presidential/contributions/by_candidate/
Net receipts per candidate. Filter with `contributor_state='US'` for national totals

**Query parameters:**
- `contributor_state` (array<string>): State of contributor
- `election_year` (array<integer>): Year of election

### GET /presidential/contributions/by_size/
Contribution receipts by size per candidate. Filter by candidate_id, election_year and/or size

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `election_year` (array<integer>): Year of election
- `size` (array<integer>, one of: 0, 200, 500, 1000, 2000): The total all contributions in the following ranges: ``` -0 $200 and under -200 $200.01 - $499.99 -500 $500 - $999.99 -1000 $1000 - $1999.9…

### GET /presidential/contributions/by_state/
Contribution receipts by state per candidate. Filter by candidate_id and/or election_year

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `election_year` (array<integer>): Year of election

### GET /presidential/coverage_end_date/
Coverage end date per candidate. Filter by candidate_id and/or election_year

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `election_year` (array<integer>): Year of election

### GET /presidential/financial_summary/
Financial summary per candidate. Filter by candidate_id and/or election_year

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `election_year` (array<integer>): Year of election
