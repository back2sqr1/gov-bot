---
name: loans
description: Schedule C shows all loans, endorsements and loan guarantees a committee receives or makes.
---

# Loans API

Schedule C shows all loans, endorsements and loan guarantees a committee receives or makes.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /schedules/schedule_c/
Schedule C shows all loans, endorsements and loan guarantees a committee receives or makes. The committee continues to report the loan until it is repaid.

**Query parameters:**
- `candidate_name` (array<string>): Name of candidate running for office
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `form_line_number` (array<string>): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `last_index` (integer): Index of last result from previous page
- `loan_source_name` (array<string>): Source of the loan (i.e., bank loan, brokerage account, credit card, home equity line of credit, other line of credit, or personal funds of…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `max_incurred_date` (string): Maximum incurred date
- `max_payment_to_date` (integer): Maximum payment to date
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `min_incurred_date` (string): Minimum incurred date
- `min_payment_to_date` (integer): Minimum payment to date

### GET /schedules/schedule_c/{sub_id}/
Schedule C shows all loans, endorsements and loan guarantees a committee receives or makes. The committee continues to report the loan until it is repaid.

**Path parameters:**
- `sub_id` (string, required)
