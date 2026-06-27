---
name: candidate
description: Candidate endpoints give you access to information about the people running for office.
---

# Candidate API

Candidate endpoints give you access to information about the people running for office. This information is organized by `candidate_id`. If you're unfamiliar with candidate IDs, using `/candidates/search/` will help you locate a particular candidate. Officially, a candidate is an individual seeking nomination for election to a federal office. People become candidates when they (or agents working on their behalf) raise contributions or make expenditures that exceed $5,000. The candidate endpoints primarily use data from FEC registration [Form 1](https://www.fec.gov/resources/cms-content/documents/fecfrm1.pdf) for committee information and [Form 2](https://www.fec.gov/resources/cms-content/documents/fecfrm2.pdf) for candidate information.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /candidate/{candidate_id}/
This endpoint is useful for finding detailed information about a particular candidate. Use the `candidate_id` to find the most recent information about that candidate.

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…

**Query parameters:**
- `candidate_status` (array<string>, one of: C, F, N, P): One-letter code explaining if the candidate is: - C present candidate - F future candidate - N not yet a candidate - P prior candidate
- `cycle` (array<integer>): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_year` (array<integer>): Year of election
- `federal_funds_flag` (boolean): A boolean the describes if a presidential candidate has accepted federal funds. The flag will be false for House and Senate candidates.
- `has_raised_funds` (boolean): A boolean that describes if a candidate's committee has ever received any receipts for their campaign for this particular office. (Candidat…
- `incumbent_challenge` (array<string>, one of: I, C, O): One-letter code ('I', 'C', 'O') explaining if the candidate is an incumbent, a challenger, or if the seat is open.
- `name` (array<string>): Name (candidate or committee) to search for. Alias for 'q'.
- `office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `state` (array<string>): US state or territory where a candidate runs for office
- `year` (string): Retrieve records pertaining to a particular election year. The list of election years is based on a candidate filing a statement of candida…

### GET /candidate/{candidate_id}/history/
Find out a candidate's characteristics over time. This is particularly useful if the candidate runs for the same office in different districts or you want to know more about a candidate's previous races. This information is organized by `candidate_id`, so it won't help you find a candidate who ran for different offices over time; candidates get a new ID for each office.

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…

**Query parameters:**
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /candidate/{candidate_id}/history/{cycle}/
Find out a candidate's characteristics over time. This is particularly useful if the candidate runs for the same office in different districts or you want to know more about a candidate's previous races. This information is organized by `candidate_id`, so it won't help you find a candidate who ran for different offices over time; candidates get a new ID for each office.

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (integer, required): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…

**Query parameters:**
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /candidate/{candidate_id}/totals/
This endpoint provides information about a committee's Form 3, Form 3X, or Form 3P financial reports, which are aggregated by two-year period. We refer to two-year periods as a `cycle`. The cycle is named after the even-numbered year and includes the year before it. To obtain totals from 2013 and 2014, you would use 2014. In odd-numbered years, the current cycle is the next year — for example, in…

**Path parameters:**
- `candidate_id` (string, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…

**Query parameters:**
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /candidates/
Fetch basic information about candidates, and use parameters to filter results to the candidates you're looking for. Each result reflects a unique FEC candidate ID. That ID is particular to the candidate for a particular office sought. If a candidate runs for the same office multiple times, the ID stays the same. If the same person runs for another office — for example, a House candidate runs for…

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `candidate_status` (array<string>, one of: C, F, N, P): One-letter code explaining if the candidate is: - C present candidate - F future candidate - N not yet a candidate - P prior candidate
- `cycle` (array<integer>): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_year` (array<integer>): Year of election
- `federal_funds_flag` (boolean): A boolean the describes if a presidential candidate has accepted federal funds. The flag will be false for House and Senate candidates.
- `has_raised_funds` (boolean): A boolean that describes if a candidate's committee has ever received any receipts for their campaign for this particular office. (Candidat…
- `incumbent_challenge` (array<string>, one of: I, C, O): One-letter code ('I', 'C', 'O') explaining if the candidate is an incumbent, a challenger, or if the seat is open.
- `is_active_candidate` (boolean): Candidates who are actively seeking office. If no value is specified, all candidates are returned. When True is specified, only active cand…
- `max_first_file_date` (string): Selects all candidates whose first filing was received by the FEC before this date.
- `min_first_file_date` (string): Selects all candidates whose first filing was received by the FEC after this date.
- `name` (array<string>): Name (candidate or committee) to search for. Alias for 'q'.
- `office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `q` (array<string>): Name of candidate running for office
- `state` (array<string>): US state or territory where a candidate runs for office
- `year` (string): Retrieve records pertaining to a particular election year. The list of election years is based on a candidate filing a statement of candida…

### GET /candidates/search/
Fetch basic information about candidates and their principal committees. Each result reflects a unique FEC candidate ID. That ID is assigned to the candidate for a particular office sought. If a candidate runs for the same office over time, that ID stays the same. If the same person runs for multiple offices — for example, a House candidate runs for a Senate office — that candidate will get a uni…

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `candidate_status` (array<string>, one of: C, F, N, P): One-letter code explaining if the candidate is: - C present candidate - F future candidate - N not yet a candidate - P prior candidate
- `cycle` (array<integer>): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_year` (array<integer>): Year of election
- `federal_funds_flag` (boolean): A boolean the describes if a presidential candidate has accepted federal funds. The flag will be false for House and Senate candidates.
- `has_raised_funds` (boolean): A boolean that describes if a candidate's committee has ever received any receipts for their campaign for this particular office. (Candidat…
- `incumbent_challenge` (array<string>, one of: I, C, O): One-letter code ('I', 'C', 'O') explaining if the candidate is an incumbent, a challenger, or if the seat is open.
- `is_active_candidate` (boolean): Candidates who are actively seeking office. If no value is specified, all candidates are returned. When True is specified, only active cand…
- `max_first_file_date` (string): Selects all candidates whose first filing was received by the FEC before this date.
- `min_first_file_date` (string): Selects all candidates whose first filing was received by the FEC after this date.
- `name` (array<string>): Name (candidate or committee) to search for. Alias for 'q'.
- `office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `q` (array<string>): Name of candidate running for office
- `state` (array<string>): US state or territory where a candidate runs for office
- `year` (string): Retrieve records pertaining to a particular election year. The list of election years is based on a candidate filing a statement of candida…

### GET /candidates/totals/
Aggregated candidate receipts and disbursements grouped by cycle.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `election_year` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `federal_funds_flag` (boolean): A boolean the describes if a presidential candidate has accepted federal funds. The flag will be false for House and Senate candidates.
- `has_raised_funds` (boolean): A boolean that describes if a candidate's committee has ever received any receipts for their campaign for this particular office. (Candidat…
- `is_active_candidate` (boolean): Candidates who are actively seeking office. If no value is specified, all candidates are returned. When True is specified, only active cand…
- `max_cash_on_hand_end_period` (number): Maximum cash on hand
- `max_debts_owed_by_committee` (number): Maximum debt
- `max_disbursements` (number): Maximum aggregated disbursements
- `max_receipts` (number): Maximum aggregated receipts
- `min_cash_on_hand_end_period` (number): Minimum cash on hand
- `min_debts_owed_by_committee` (number): Minimum debt
- `min_disbursements` (number): Minimum aggregated disbursements
- `min_receipts` (number): Minimum aggregated receipts
- `office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `party` (array<string>): Three-letter party code
- `q` (array<string>): Name of candidate running for office
- `state` (array<string>): US state or territory where a candidate runs for office

### GET /candidates/totals/aggregates/
Candidate total receipts and disbursements aggregated by `aggregate_by`.

**Query parameters:**
- `aggregate_by` (string, one of: office, office-state, office-state-district, office-party): Candidate totals aggregate_by (Chose one of dropdown options): - ' ' grouped by election year - office grouped by election year, by office…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `election_year` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `is_active_candidate` (boolean): Candidates who are actively seeking office. If no value is specified, all candidates are returned. When True is specified, only active cand…
- `max_election_cycle` (integer): Filter records to only those that are applicable to a given two-year period. This cycle follows the traditional House election cycle and su…
- `min_election_cycle` (integer): Filter records to only those that are applicable to a given two-year period. This cycle follows the traditional House election cycle and su…
- `office` (string, one of: H, S, P): Federal office candidate runs for: H, S or P
- `party` (string, one of: DEM, REP, OTHER): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `state` (array<string>): US state or territory where a candidate runs for office

### GET /committee/{committee_id}/candidates/
This endpoint is useful for finding detailed information about a particular candidate. Use the `candidate_id` to find the most recent information about that candidate.

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…

**Query parameters:**
- `candidate_status` (array<string>, one of: C, F, N, P): One-letter code explaining if the candidate is: - C present candidate - F future candidate - N not yet a candidate - P prior candidate
- `cycle` (array<integer>): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_year` (array<integer>): Year of election
- `federal_funds_flag` (boolean): A boolean the describes if a presidential candidate has accepted federal funds. The flag will be false for House and Senate candidates.
- `has_raised_funds` (boolean): A boolean that describes if a candidate's committee has ever received any receipts for their campaign for this particular office. (Candidat…
- `incumbent_challenge` (array<string>, one of: I, C, O): One-letter code ('I', 'C', 'O') explaining if the candidate is an incumbent, a challenger, or if the seat is open.
- `name` (array<string>): Name (candidate or committee) to search for. Alias for 'q'.
- `office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `state` (array<string>): US state or territory where a candidate runs for office
- `year` (string): Retrieve records pertaining to a particular election year. The list of election years is based on a candidate filing a statement of candida…

### GET /committee/{committee_id}/candidates/history/
Find out a candidate's characteristics over time. This is particularly useful if the candidate runs for the same office in different districts or you want to know more about a candidate's previous races. This information is organized by `candidate_id`, so it won't help you find a candidate who ran for different offices over time; candidates get a new ID for each office.

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…

**Query parameters:**
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /committee/{committee_id}/candidates/history/{cycle}/
Find out a candidate's characteristics over time. This is particularly useful if the candidate runs for the same office in different districts or you want to know more about a candidate's previous races. This information is organized by `candidate_id`, so it won't help you find a candidate who ran for different offices over time; candidates get a new ID for each office.

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (integer, required): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…

**Query parameters:**
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
