---
name: committee
description: Committees are entities that spend and raise money in an election.
---

# Committee API

Committees are entities that spend and raise money in an election. Their characteristics and relationships with candidates can change over time. You might want to use filters or search endpoints to find the committee you're looking for. Then you can use other committee endpoints to explore information about the committee that interests you. Financial information is organized by `committee_id`, so finding the committee you're interested in will lead you to more granular financial information. The committee endpoints include all FEC filers, even if they aren't registered as a committee. Officially, committees include the committees and organizations that file with the FEC. Several different types of organizations file financial reports with the FEC: *Campaign committees authorized by particular candidates to raise and spend funds in their campaigns. Non-party committees (e.g., PACs), some of which may be sponsored by corporations, unions, trade or membership groups, etc. Political party committees at the national, state, and local levels. Groups and individuals making only independent expenditures Corporations, unions, and other organizations making internal communications* The committee endpoints primarily use data from FEC registration Form 1 and Form 2.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /candidate/{candidate_id}/committees/
This endpoint is useful for finding detailed information about a particular committee or filer. Use the `committee_id` to find the most recent information about the committee.

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…

**Query parameters:**
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): A two year election cycle that the committee was active- (after original registration date but before expiration date in Form 1s) The cycle…
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `filing_frequency` (array<string>, one of: A, M, N, Q, T, W, -A, -T): The one-letter code of the filing frequency: - A Administratively terminated - D Debt - M Monthly filer - Q Quarterly filer - T Terminated…
- `organization_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `year` (array<integer>): A year that the committee was active— (after original registration date or filing but before expiration date)

### GET /candidate/{candidate_id}/committees/history/
Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`.

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…

**Query parameters:**
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /candidate/{candidate_id}/committees/history/{cycle}/
Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`.

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (integer, required): A two year election cycle that the committee was active- (after original registration date but before expiration date in Form 1s) The cycle…

**Query parameters:**
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /committee/{committee_id}/
This endpoint is useful for finding detailed information about a particular committee or filer. Use the `committee_id` to find the most recent information about the committee.

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…

**Query parameters:**
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): A two year election cycle that the committee was active- (after original registration date but before expiration date in Form 1s) The cycle…
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `filing_frequency` (array<string>, one of: A, M, N, Q, T, W, -A, -T): The one-letter code of the filing frequency: - A Administratively terminated - D Debt - M Monthly filer - Q Quarterly filer - T Terminated…
- `organization_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `year` (array<integer>): A year that the committee was active— (after original registration date or filing but before expiration date)

### GET /committee/{committee_id}/history/
Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`.

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…

**Query parameters:**
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /committee/{committee_id}/history/{cycle}/
Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`.

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (integer, required): A two year election cycle that the committee was active- (after original registration date but before expiration date in Form 1s) The cycle…

**Query parameters:**
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /committees/
Fetch basic information about committees and filers. Use parameters to filter for particular characteristics.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): A two year election cycle that the committee was active- (after original registration date but before expiration date in Form 1s) The cycle…
- `designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `filing_frequency` (array<string>, one of: A, M, N, Q, T, W, -A, -T): The one-letter code of the filing frequency: - A Administratively terminated - D Debt - M Monthly filer - Q Quarterly filer - T Terminated…
- `max_first_f1_date` (string): Filter for committees whose first Form 1 was received on or before this date.
- `max_first_file_date` (string): Filter for committees whose first filing was received on or before this date.
- `max_last_f1_date` (string): Filter for committees whose latest Form 1 was received on or before this date.
- `max_last_file_date` (string): Filter for committees whose last filing was received on or before this date.
- `min_first_f1_date` (string): Filter for committees whose first Form 1 was received on or after this date.
- `min_first_file_date` (string): Filter for committees whose first filing was received on or after this date.
- `min_last_f1_date` (string): Filter for committees whose latest Form 1 was received on or after this date.
- `min_last_file_date` (string): Filter for committees whose last filing was received on or after this date.
- `organization_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `q` (array<string>): The name of the committee. If a committee changes its name, the most recent name will be shown. Committee names are not unique. Use committ…
- `sponsor_candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `state` (array<string>): A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and any invalid or missin…
- `treasurer_name` (array<string>): Name of the Committee's treasurer. If multiple treasurers for the committee, the most recent treasurer will be shown.
- `year` (array<integer>): A year that the committee was active— (after original registration date or filing but before expiration date)
