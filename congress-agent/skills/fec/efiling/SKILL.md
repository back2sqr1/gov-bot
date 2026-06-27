---
name: efiling
description: Efiling endpoints provide real-time campaign finance data received from electronic filers.
---

# Efiling API

Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /efile/filings/
Basic information about electronic files coming into the FEC, posted as they are received.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `file_number` (array<integer>): Filing ID number
- `form_type` (array<string>): The form where the underlying data comes from, for example Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `max_receipt_date` (string): Selects all filings received before this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_receipt_date` (string): Selects all filings received after this date(MM/DD/YYYY or YYYY-MM-DD)
- `q_filer` (array<string>): Keyword search for filer name or ID

### GET /efile/form1/
Basic information about electronic files coming into the FEC, posted as they are received.

**Query parameters:**
- `candidate_district` (array<string>): House district of the office sought, if applicable.
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `candidate_office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `candidate_party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `election_state` (array<string>): State or territory of the office sought.
- `file_number` (array<string>): Filing ID number
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_load_timestamp` (string): Date the information was loaded into the FEC systems. This can be affected by reseting systems and other factors, refer to receipt_date for…
- `min_load_timestamp` (string): Date the information was loaded into the FEC systems. This can be affected by reseting systems and other factors, refer to receipt_date for…
- `organization_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…

### GET /efile/form2/
Basic information about electronic files coming into the FEC, posted as they are received.

**Query parameters:**
- `candidate_district` (array<string>): House district of the office sought, if applicable.
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `candidate_office` (array<string>, one of: H, S, P): Federal office candidate runs for: H, S or P
- `candidate_party` (array<string>): Three-letter code for the party affiliated with a candidate or committee. For example, DEM for Democratic Party and REP for Republican Part…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `election_state` (array<string>): State or territory of the office sought.
- `file_number` (array<integer>): Filing ID number
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_load_timestamp` (string): Date the information was loaded into the FEC systems. This can be affected by reseting systems and other factors, refer to receipt_date for…
- `min_load_timestamp` (string): Date the information was loaded into the FEC systems. This can be affected by reseting systems and other factors, refer to receipt_date for…

### GET /efile/reports/house-senate/
Key financial data reported periodically by committees as they are reported. This feed includes summary information from the the House F3 reports, the presidential F3p reports and the PAC and party F3x reports. Generally, committees file reports on a quarterly or monthly basis, but some must also submit a report 12 days before primary elections. Therefore, during the primary season, the period co…

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `file_number` (array<integer>): Filing ID number
- `form_type` (array<string>): The form where the underlying data comes from, for example Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `max_receipt_date` (string): Selects all filings received before this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_receipt_date` (string): Selects all filings received after this date(MM/DD/YYYY or YYYY-MM-DD)
- `q_filer` (array<string>): Keyword search for filer name or ID

### GET /efile/reports/pac-party/
Key financial data reported periodically by committees as they are reported. This feed includes summary information from the the House F3 reports, the presidential F3p reports and the PAC and party F3x reports. Generally, committees file reports on a quarterly or monthly basis, but some must also submit a report 12 days before primary elections. Therefore, during the primary season, the period co…

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `file_number` (array<integer>): Filing ID number
- `form_type` (array<string>): The form where the underlying data comes from, for example Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `max_receipt_date` (string): Selects all filings received before this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_receipt_date` (string): Selects all filings received after this date(MM/DD/YYYY or YYYY-MM-DD)
- `q_filer` (array<string>): Keyword search for filer name or ID

### GET /efile/reports/presidential/
Key financial data reported periodically by committees as they are reported. This feed includes summary information from the the House F3 reports, the presidential F3p reports and the PAC and party F3x reports. Generally, committees file reports on a quarterly or monthly basis, but some must also submit a report 12 days before primary elections. Therefore, during the primary season, the period co…

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `file_number` (array<integer>): Filing ID number
- `form_type` (array<string>): The form where the underlying data comes from, for example Form 1 would appear as F1: - F1 Statement of Organization - F1M Notification of…
- `max_receipt_date` (string): Selects all filings received before this date(MM/DD/YYYY or YYYY-MM-DD)
- `min_receipt_date` (string): Selects all filings received after this date(MM/DD/YYYY or YYYY-MM-DD)
- `q_filer` (array<string>): Keyword search for filer name or ID
