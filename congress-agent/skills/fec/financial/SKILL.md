---
name: financial
description: Fetch key information about a committee's Form 3, Form 3X, Form 13, or Form 3P financial reports.
---

# Financial API

Fetch key information about a committee's Form 3, Form 3X, Form 13, or Form 3P financial reports. Most committees are required to summarize their financial activity in each filing; those summaries are included in these files. Generally, committees file reports on a quarterly or monthly basis, but some must also submit a report 12 days before primary elections. Therefore, during the primary season, the period covered by this file may be different for different committees. These totals also incorporate any changes made by committees, if any report covering the period is amended. Information is made available on the API as soon as it's processed. Keep in mind, complex paper filings take longer to process. The financial endpoints use data from FEC [form 5](https://www.fec.gov/pdf/forms/fecfrm5.pdf), for independent expenditors; or the summary and detailed summary pages of the FEC [Form 3](https://www.fec.gov/pdf/forms/fecfrm3.pdf), for House and Senate committees; [Form 3X](https://www.fec.gov/pdf/forms/fecfrm3x.pdf), for PACs and parties; [Form 13](https://www.fec.gov/pdf/forms/fecfrm13.pdf) for inaugural committees; and [Form 3P](https://www.fec.gov/pdf/forms/fecfrm3p.pdf), for presidential committees.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /committee/{committee_id}/reports/
Each report represents the summary information from Form 3, Form 3X and Form 3P. These reports have key statistics that illuminate the financial status of a given committee. Things like cash on hand, debts owed by committee, total receipts, and total disbursements are especially helpful for understanding a committee's financial dealings. By default, this endpoint includes both amended and final v…

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…

**Query parameters:**
- `beginning_image_number` (array<string>): Unique identifier for the electronic or paper report. This number is used to construct PDF URLs to the original document.
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `is_amended` (boolean): False indicates that a report is the most recent. True indicates that the report has been superseded by an amendment.
- `max_cash_on_hand_end_period_amount` (number): Filter for all amounts less than a value.
- `max_debts_owed_expenditures` (number): Filter for all amounts less than a value.
- `max_disbursements_amount` (number): Filter for all amounts less than a value.
- `max_independent_expenditures` (number): Filter for all amounts less than a value.
- `max_party_coordinated_expenditures` (number): Filter for all amounts less than a value.
- `max_receipts_amount` (number): Filter for all amounts less than a value.
- `max_total_contributions` (number): Filter for all amounts less than a value.
- `min_cash_on_hand_end_period_amount` (number): Filter for all amounts greater than a value.
- `min_debts_owed_amount` (number): Filter for all amounts greater than a value.
- `min_disbursements_amount` (number): Filter for all amounts greater than a value.
- `min_independent_expenditures` (number): Filter for all amounts greater than a value.
- `min_party_coordinated_expenditures` (number): Filter for all amounts greater than a value.
- `min_receipts_amount` (number): Filter for all amounts greater than a value.
- `min_total_contributions` (number): Filter for all amounts greater than a value.
- `report_type` (array<string>): Report type; prefix with "-" to exclude. Name of report where the underlying data comes from: - 10D Pre-Election - 10G Pre-General - 10P Pr…
- `type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.

### GET /committee/{committee_id}/totals/
This endpoint provides information about a committee's Form 3, Form 3X, or Form 3P financial reports, which are aggregated by two-year period. We refer to two-year periods as a `cycle`. The cycle is named after the even-numbered year and includes the year before it. To obtain totals from 2013 and 2014, you would use 2014. In odd-numbered years, the current cycle is the next year — for example, in…

**Path parameters:**
- `committee_id` (string, required): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…

**Query parameters:**
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…

### GET /elections/
Look at the top-level financial information for all candidates running for the same office. Choose a 2-year cycle, and `house`, `senate` or `presidential`. If you are looking for a Senate seat, you will need to select the state using a two-letter abbreviation. House races require state and a two-digit district number. Since this endpoint reflects financial information, it will only have candidate…

**Query parameters:**
- `cycle` (integer, required): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `office` (string, required, one of: house, senate, president): Federal office candidate runs for: H, S or P
- `district` (string): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `state` (string): US state or territory where a candidate runs for office

### GET /elections/search/
List elections by cycle, office, state, and district.

**Query parameters:**
- `cycle` (array<integer>): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `office` (array<string>, one of: house, senate, president)
- `state` (array<string>): US state or territory where a candidate runs for office
- `zip` (array<integer>): Zip code

### GET /elections/summary/
List elections by cycle, office, state, and district.

**Query parameters:**
- `cycle` (integer, required): Two-year election cycle in which a candidate runs for office. Calculated from Form 2. The cycle begins with an odd year and is named for it…
- `office` (string, required, one of: house, senate, president): Federal office candidate runs for: H, S or P
- `district` (string): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `state` (string): US state or territory where a candidate runs for office

### GET /reports/{entity_type}/
Each report represents the summary information from Form 3, Form 3X and Form 3P. These reports have key statistics that illuminate the financial status of a given committee. Things like cash on hand, debts owed by committee, total receipts, and total disbursements are especially helpful for understanding a committee's financial dealings. By default, this endpoint includes both amended and final v…

**Path parameters:**
- `entity_type` (string, required, one of: presidential, pac-party, house-senate, ie-only): Committee groupings based on FEC filing form. Choose one of: `presidential`, `pac-party`, `house-senate`, or `ie-only`

**Query parameters:**
- `amendment_indicator` (array<string>, one of: N, A, T, C, M, S): Amendent types: -N new -A amendment -T terminated -C consolidated -M multi-candidate -S secondary NULL might be new or amendment. If amendm…
- `beginning_image_number` (array<string>): Unique identifier for the electronic or paper report. This number is used to construct PDF URLs to the original document.
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `filer_type` (string, one of: e-file, paper): The method used to file with the FEC, either electronic or on paper.
- `is_amended` (boolean): False indicates that a report is the most recent. True indicates that the report has been superseded by an amendment.
- `max_cash_on_hand_end_period_amount` (number): Filter for all amounts less than a value.
- `max_debts_owed_expenditures` (number): Filter for all amounts less than a value.
- `max_disbursements_amount` (number): Filter for all amounts less than a value.
- `max_independent_expenditures` (number): Filter for all amounts less than a value.
- `max_party_coordinated_expenditures` (number): Filter for all amounts less than a value.
- `max_receipt_date` (string): Selects all items received by FEC before this date(MM/DD/YYYY or YYYY-MM-DD)
- `max_receipts_amount` (number): Filter for all amounts less than a value.
- `max_total_contributions` (number): Filter for all amounts less than a value.
- `min_cash_on_hand_end_period_amount` (number): Filter for all amounts greater than a value.
- `min_debts_owed_amount` (number): Filter for all amounts greater than a value.
- `min_disbursements_amount` (number): Filter for all amounts greater than a value.
- `min_independent_expenditures` (number): Filter for all amounts greater than a value.
- `min_party_coordinated_expenditures` (number): Filter for all amounts greater than a value.
- `min_receipt_date` (string): Selects all items received by FEC after this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_receipts_amount` (number): Filter for all amounts greater than a value.
- `min_total_contributions` (number): Filter for all amounts greater than a value.
- `most_recent` (boolean): Report is either new or is the most-recently filed amendment
- `q_filer` (array<string>): Keyword search for filer name or ID
- `q_spender` (array<string>): Keyword search for spender name or ID
- `report_type` (array<string>): Report type; prefix with "-" to exclude. Name of report where the underlying data comes from: - 10D Pre-Election - 10G Pre-General - 10P Pr…
- `year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.

### GET /totals/by_entity/
Provides cumulative receipt totals by entity type, over a two year cycle. Totals are adjusted to avoid double counting. This is [the sql](https://github.com/fecgov/openFEC/blob/develop/data/migrations/V41__large_aggregates.sql) that creates these calculations.

**Query parameters:**
- `cycle` (integer, required): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…

### GET /totals/inaugural_committees/by_contributor/
This endpoint provides information about an inaugural committee's Form 13 report of donations accepted. The data is aggregated by the contributor and the two-year period. We refer to two-year periods as a `cycle`.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `contributor_name` (array<string>): Name of contributor
- `cycle` (array<integer>): A two year election cycle that the committee was active- (after original registration date but before expiration date in Form 1s) The cycle…

### GET /totals/{entity_type}/
This endpoint provides information about a committee's Form 3, Form 3X, or Form 3P financial reports, which are aggregated by two-year period. We refer to two-year periods as a `cycle`. The cycle is named after the even-numbered year and includes the year before it. To obtain totals from 2013 and 2014, you would use 2014. In odd-numbered years, the current cycle is the next year — for example, in…

**Path parameters:**
- `entity_type` (string, required, one of: presidential, pac, party, pac-party, house-senate, ie-only): Committee groupings based on FEC filing form. Choose one of: `presidential`, `pac`, `party`, `pac-party`, `house-senate`, or `ie-only`

**Query parameters:**
- `committee_designation` (array<string>): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `committee_state` (array<string>): A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and any invalid or missin…
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `filing_frequency` (array<string>, one of: A, M, N, Q, T, W, -A, -T): The one-letter code of the filing frequency: - A Administratively terminated - D Debt - M Monthly filer - Q Quarterly filer - T Terminated…
- `max_disbursements` (number): Filter for all amounts less than a value.
- `max_first_f1_date` (string): Filter for committees whose first Form 1 was received on or before this date.
- `max_last_cash_on_hand_end_period` (number): Filter for all amounts less than a value.
- `max_last_debts_owed_by_committee` (number): Filter for all amounts less than a value.
- `max_receipts` (number): Filter for all amounts less than a value.
- `min_disbursements` (number): Filter for all amounts greater than a value.
- `min_first_f1_date` (string): Filter for committees whose first Form 1 was received on or after this date.
- `min_last_cash_on_hand_end_period` (number): Filter for all amounts greater than a value.
- `min_last_debts_owed_by_committee` (number): Filter for all amounts greater than a value.
- `min_receipts` (number): Filter for all amounts greater than a value.
- `organization_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `sponsor_candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `treasurer_name` (array<string>): Name of the Committee's treasurer. If multiple treasurers for the committee, the most recent treasurer will be shown.
