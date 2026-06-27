---
name: independent-expenditures
description: Schedule E covers the line item expenditures for independent expenditures.
---

# Independent Expenditures API

Schedule E covers the line item expenditures for independent expenditures. For example, if a super PAC bought ads on TV to oppose a federal candidate, each ad purchase would be recorded here with the expenditure amount, name and id of the candidate, and whether the ad supported or opposed the candidate. An independent expenditure is an expenditure for a communication "expressly advocating the election or defeat of a clearly identified candidate that is not made in cooperation, consultation, or concert with, or at the request or suggestion of, a candidate, a candidate’s authorized committee, or their agents, or a political party or its agents." Aggregates by candidate do not include 24 and 48 hour reports. This ensures we don't double count expenditures and the totals are more accurate. You can still find the information from 24 and 48 hour reports in `/schedule/schedule_e/`.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /schedules/schedule_e/
Schedule E covers the line item expenditures for independent expenditures. For example, if a super PAC bought ads on TV to oppose a federal candidate, each ad purchase would be recorded here with the expenditure amount, name and id of the candidate, and whether the ad supported or opposed the candidate. An independent expenditure is an expenditure for a communication "expressly advocating the ele…

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `candidate_office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `candidate_office_district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `candidate_office_state` (array<string>): A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and any invalid or missin…
- `candidate_party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `filing_form` (array<string>): The form where the underlying data comes from, for example, Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `form_line_number` (array<string>): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `is_notice` (array<boolean>): Record filed as 24- or 48-hour notice.
- `last_expenditure_amount` (number): When sorting by `expenditure_amount`, this is populated with the `expenditure_amount` of the last result. However, you will need to pass th…
- `last_expenditure_date` (string): When sorting by `expenditure_date`, this is populated with the `expenditure_date` of the last result. However, you will need to pass the in…
- `last_index` (integer): Index of last result from previous page
- `last_office_total_ytd` (number): When sorting by `office_total_ytd`, this is populated with the `office_total_ytd` of the last result. However, you will need to pass the in…
- `last_support_oppose_indicator` (string): When sorting by `support_oppose_indicator`, this is populated with the `support_oppose_indicator` of the last result. However, you will nee…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_dissemination_date` (string): Selects all items distributed by this committee before this date
- `max_filing_date` (string): Selects all filings received before this date
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_dissemination_date` (string): Selects all items distributed by this committee after this date
- `min_filing_date` (string): Selects all filings received after this date
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `most_recent` (boolean): The report associated with the transaction is either new or is the most-recently filed amendment. Undetermined version (`null`) is always i…
- `payee_name` (array<string>): Name of the entity that received the payment.
- `q_spender` (array<string>): Keyword search for spender name or ID
- `support_oppose_indicator` (array<string>, one of: S, O): Explains if the money was spent in order to support or oppose a candidate or candidates. (Coded S or O for support or oppose.) This indicat…

### GET /schedules/schedule_e/by_candidate/
Schedule E receipts aggregated by recipient candidate. To avoid double counting, memoed items are not included.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `district` (string): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
- `office` (string, one of: house, senate, president): Federal office candidate runs for: H, S or P
- `state` (string): US state or territory where a candidate runs for office
- `support_oppose` (string, one of: S, O): Support or opposition

### GET /schedules/schedule_e/efile/
Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `candidate_office` (string, one of: H, S, P): Federal office candidate runs for: H, S or P
- `candidate_office_district` (array<string>): Two-digit US House distirict of the office the candidate is running for. Presidential, Senate and House at-large candidates will have Distr…
- `candidate_office_state` (array<string>): US state or territory where a candidate runs for office
- `candidate_party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `candidate_search` (array<string>): Search for candidates by candiate id or candidate first or last name
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `filing_form` (array<string>): The form where the underlying data comes from, for example, Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `is_notice` (boolean): Record filed as 24- or 48-hour notice.
- `max_dissemination_date` (string): Selects all items distributed by this committee before this date
- `max_expenditure_amount` (integer): Selects all items expended by this committee less than this amount
- `max_expenditure_date` (string): Selects all items expended by this committee before this date
- `max_filed_date` (string): Timestamp of electronic or paper record that FEC received
- `min_dissemination_date` (string): Selects all items distributed by this committee after this date
- `min_expenditure_amount` (integer): Selects all items expended by this committee greater than this amount
- `min_expenditure_date` (string): Selects all items expended by this committee after this date
- `min_filed_date` (string): Timestamp of electronic or paper record that FEC received
- `most_recent` (boolean): The report associated with the transaction is either new or is the most-recently filed amendment. Undetermined version (`null`) is always i…
- `payee_name` (array<string>): Name of the entity that received the payment.
- `spender_name` (array<string>): The name of the committee. If a committee changes its name, the most recent name will be shown. Committee names are not unique. Use committ…
- `support_oppose_indicator` (array<string>, one of: S, O): Explains if the money was spent in order to support or oppose a candidate or candidates. (Coded S or O for support or oppose.) This indicat…

### GET /schedules/schedule_e/totals/by_candidate/
Total independent expenditure on supported or opposed candidates by cycle or candidate election year.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.
