---
name: debts
description: Schedule D, it shows debts and obligations owed to or by the committee that are required to be disclosed.
---

# Debts API

Schedule D, it shows debts and obligations owed to or by the committee that are required to be disclosed.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /schedules/schedule_d/
Schedule D, it shows debts and obligations owed to or by the committee that are required to be disclosed.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `creditor_debtor_name` (array<string>)
- `filing_form` (array<string>): The form where the underlying data comes from, for example, Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `form_line_number` (array<string>): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_amount_incurred` (number)
- `max_amount_outstanding_beginning` (number)
- `max_amount_outstanding_close` (number)
- `max_coverage_end_date` (string): Ending date of the reporting period before this date(MM/DD/YYYY or YYYY-MM-DD)
- `max_coverage_start_date` (string): Starting date of the reporting period before this date(MM/DD/YYYY or YYYY-MM-DD)
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `max_payment_period` (number)
- `min_amount_incurred` (number)
- `min_amount_outstanding_beginning` (number)
- `min_amount_outstanding_close` (number)
- `min_coverage_end_date` (string): Ending date of the reporting period after this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_coverage_start_date` (string): Starting date of the reporting period after this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `min_payment_period` (number)
- `nature_of_debt` (string)
- `report_type` (array<string>): Name of report where the underlying data comes from: - 10D Pre-Election - 10G Pre-General - 10P Pre-Primary - 10R Pre-Run-Off - 10S Pre-Spe…
- `report_year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.

### GET /schedules/schedule_d/{sub_id}/
Schedule D, it shows debts and obligations owed to or by the committee that are required to be disclosed.

**Path parameters:**
- `sub_id` (string, required)
