---
name: communication-cost
description: Reports of communication costs by corporations and membership organizations from the FEC [F7 forms](https://www.fec.gov/pdf/forms/fecform7.pdf).
---

# Communication Cost API

Reports of communication costs by corporations and membership organizations from the FEC [F7 forms](https://www.fec.gov/pdf/forms/fecform7.pdf).

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /communication_costs/
52 U.S.C. 30118 allows "communications by a corporation to its stockholders and executive or administrative personnel and their families or by a labor organization to its members and their families on any subject," including the express advocacy of the election or defeat of any Federal candidate. The costs of such communications must be reported to the Federal Election Commission under certain ci…

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `support_oppose_indicator` (array<string>, one of: S, O): Support or opposition

### GET /communication_costs/aggregates/
Communication cost aggregated by candidate ID and committee ID.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `support_oppose_indicator` (string, one of: S, O): Support or opposition

### GET /communication_costs/by_candidate/
Communication cost aggregated by candidate ID and committee ID.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `district` (string): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `office` (string, one of: house, senate, president): Federal office candidate runs for: H, S or P
- `state` (string): US state or territory where a candidate runs for office
- `support_oppose` (string, one of: S, O): Support or opposition

### GET /communication_costs/totals/by_candidate/
Total communications costs aggregated across committees on supported or opposed candidates by cycle or candidate election year.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
