---
name: national-party-accounts
description: Collection of endpoints that provide information about national party committee accounts including presidential nominating conventions, national party headquarters buildings, and election recounts an…
---

# National Party Accounts API

Collection of endpoints that provide information about national party committee accounts including presidential nominating conventions, national party headquarters buildings, and election recounts and contests and other legal proceedings accounts.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /national_party/schedule_a/
This endpoint includes national party committee account receipts for presidential nominating conventions, national party headquarters buildings, and election recounts and contests and other legal proceedings accounts.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `contributor_city` (array<string>): City of contributor
- `contributor_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `contributor_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `contributor_employer` (array<string>): Employer of contributor, filers need to make an effort to gather this information
- `contributor_id` (array<string>): The FEC identifier should be represented here if the contributor is registered with the FEC.
- `contributor_name` (array<string>): Name of contributor
- `contributor_occupation` (array<string>): Occupation of contributor, filers need to make an effort to gather this information
- `contributor_state` (array<string>): State of contributor. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and…
- `contributor_type` (array<string>, one of: individual, committee): Filters individual or committee contributions based on line number
- `contributor_zip` (array<string>): Zip code of contributor
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `is_individual` (boolean): Restrict to non-earmarked individual contributions where memo code is true. Filtering individuals is useful to make sure contributions are…
- `max_contribution_receipt_amount` (number): Maximum receipts amount
- `max_contribution_receipt_date` (string): Selects all filings received before this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_contribution_receipt_amount` (number): Minimum receipts amount
- `min_contribution_receipt_date` (string): Selects all filings received after this date(MM/DD/YYYY or YYYY-MM-DD)
- `party_account_type` (array<string>, one of: CONVENTION, HEADQUARTERS, RECOUNT): Type of national party account: - CONVENTION - HEADQUARTERS - RECOUNT
- `receipt_type` (array<string>): National party account receipt types: -30 CONVENTION ACCOUNT RECEIPT - INDIVIDUAL -30E EARMARKED – CONVENTION -30F MEMO RECEIPT FROM REGIST…
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…

### GET /national_party/schedule_b/
This endpoint includes national party committee account disbursements for presidential nominating conventions, national party headquarters buildings, and election recounts and contests and other legal proceedings accounts

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `disbursement_description` (array<string>): Description of disbursement
- `disbursement_purpose_category` (array<string>, one of: ADMINISTRATIVE, ADVERTISING, CONTRIBUTIONS, EVENTS, FUNDRAISING, LOAN-REPAYMENTS, MATERIALS, OTHER, POLLING, REFUNDS, TRANSFERS, TRAVEL): Disbursement purpose category
- `disbursement_type` (array<string>, one of: 40, 40T, 40Y, 40Z, 41, 41T, 41Y, 41Z, 42, 42T, 42Y, 42Z): National party account disbursement types: -40 CONVENTION ACCOUNT DISBURSEMENT -40T CONVENTION ACCOUNT REFUND - TRIBAL -40Y CONVENTION ACCO…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `line_number` (string): Filter for form and line number using the following format: `<form_number-line_number>`. For example F3X-21b or F3X-29 would filter down to…
- `max_disbursement_amount` (number): Maximum disbursement amount
- `max_disbursement_date` (string): Selects all disbursements received before this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_disbursement_amount` (number): Minimum disbursement amount
- `min_disbursement_date` (string): Selects all disbursements received after this date(MM/DD/YYYY or YYYY-MM-DD)
- `party_account_type` (array<string>, one of: CONVENTION, HEADQUARTERS, RECOUNT): Type of national party account: - CONVENTION - HEADQUARTERS - RECOUNT
- `recipient_city` (array<string>): City of recipient
- `recipient_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `recipient_committee_id` (array<string>): The FEC identifier should be represented here if the contributor is registered with the FEC.
- `recipient_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `recipient_name` (array<string>): Name of the entity receiving the disbursement
- `recipient_state` (array<string>): State of recipient. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and a…
- `recipient_zip` (array<string>): Zipcode of recipient
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…

### GET /national_party/totals/
This endpoint includes national party committee account total receipts and total disbursements for presidential nominating conventions, national party headquarters buildings, and election recounts and contests and other legal proceedings accounts for a given two year cycle.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…
