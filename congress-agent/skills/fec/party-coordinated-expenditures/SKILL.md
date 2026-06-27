---
name: party-coordinated-expenditures
description: Schedule F, it shows all special expenditures a national or state party committee makes in connection with the general election campaigns of federal candidates.
---

# Party-Coordinated Expenditures API

Schedule F, it shows all special expenditures a national or state party committee makes in connection with the general election campaigns of federal candidates.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /schedules/schedule_f/
Schedule F, it shows all special expenditures a national or state party committee makes in connection with the general election campaigns of federal candidates. These coordinated party expenditures do not count against the contribution limits but are subject to other limits, these limits are detailed in Chapter 7 of the FEC Campaign Guide for Political Party Committees.

**Query parameters:**
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `form_line_number` (array<string>): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `payee_name` (array<string>): Name of the entity that received the payment.

### GET /schedules/schedule_f/{sub_id}/
Schedule F, it shows all special expenditures a national or state party committee makes in connection with the general election campaigns of federal candidates. These coordinated party expenditures do not count against the contribution limits but are subject to other limits, these limits are detailed in Chapter 7 of the FEC Campaign Guide for Political Party Committees.

**Path parameters:**
- `sub_id` (string, required)
