---
name: electioneering
description: An electioneering communication is any broadcast, cable or satellite communication that fulfills each of the following conditions: _The communication refers to a clearly identified federal candidate.…
---

# Electioneering API

An electioneering communication is any broadcast, cable or satellite communication that fulfills each of the following conditions: _The communication refers to a clearly identified federal candidate._ _The communication is publicly distributed by a television station, radio station, cable television system or satellite system for a fee._ _The communication is distributed within 60 days prior to a general election or 30 days prior to a primary election to federal office._

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /electioneering/
An electioneering communication is any broadcast, cable or satellite communication that fulfills each of the following conditions: _The communication refers to a clearly identified federal candidate._ _The communication is publicly distributed by a television station, radio station, cable television system or satellite system for a fee._ _The communication is distributed within 60 days prior to a…

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `disbursement_description` (array<string>): Description of disbursement
- `last_index` (integer): Index of last result from previous page
- `max_amount` (number): Filter for all amounts less than a value
- `max_date` (string): Maximum disbursement date
- `min_amount` (number): Filter for all amounts greater than a value
- `min_date` (string): Minimum disbursement date
- `report_year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.

### GET /electioneering/aggregates/
Electioneering communications costs aggregates

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…

### GET /electioneering/by_candidate/
Electioneering costs aggregated by candidate

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `district` (string): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `office` (string, one of: house, senate, president): Federal office candidate runs for: H, S or P
- `state` (string): US state or territory where a candidate runs for office

### GET /electioneering/totals/by_candidate/
Total electioneering communications spent on candidates by cycle or candidate election year

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
