---
name: dates
description: Reporting deadlines, election dates FEC meetings, events etc.
---

# Dates API

Reporting deadlines, election dates FEC meetings, events etc.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /calendar-dates/
Combines the election and reporting dates with Commission meetings, conferences, outreach, Advisory Opinions, rules, litigation dates and other events into one calendar. State and report type filtering is no longer available.

**Query parameters:**
- `calendar_category_id` (array<integer>): Each type of event has a calendar category with an integer id. Options are: Open Meetings: 32, Executive Sessions: 39, Public Hearings: 40,…
- `description` (array<string>): Brief description of event
- `event_id` (integer): An unique ID for an event. Useful for downloading a single event to your calendar. This ID is not a permanent, persistent ID.
- `max_end_date` (string): The maximum end date.(MM/DD/YYYY or YYYY-MM-DD)
- `max_start_date` (string): The maximum start date.(MM/DD/YYYY or YYYY-MM-DD)
- `min_end_date` (string): The minimum end date.(MM/DD/YYYY or YYYY-MM-DD)
- `min_start_date` (string): The minimum start date.(MM/DD/YYYY or YYYY-MM-DD)
- `summary` (array<string>): Longer description of event

### GET /calendar-dates/export/
Returns CSV or ICS for downloading directly into calendar applications like Google, Outlook or other applications. Combines the election and reporting dates with Commission meetings, conferences, outreach, Advisory Opinions, rules, litigation dates and other events into one calendar. State filtering now applies to elections, reports and reporting periods. Presidential pre-primary report due dates…

**Query parameters:**
- `calendar_category_id` (array<integer>): Each type of event has a calendar category with an integer id. Options are: Open Meetings: 32, Executive Sessions: 39, Public Hearings: 40,…
- `description` (array<string>): Brief description of event
- `event_id` (integer): An unique ID for an event. Useful for downloading a single event to your calendar. This ID is not a permanent, persistent ID.
- `max_end_date` (string): The maximum end date.(MM/DD/YYYY or YYYY-MM-DD)
- `max_start_date` (string): The maximum start date.(MM/DD/YYYY or YYYY-MM-DD)
- `min_end_date` (string): The minimum end date.(MM/DD/YYYY or YYYY-MM-DD)
- `min_start_date` (string): The minimum start date.(MM/DD/YYYY or YYYY-MM-DD)
- `renderer` (string, one of: ics, csv)
- `summary` (array<string>): Longer description of event

### GET /election-dates/
FEC election dates since 1995.

**Query parameters:**
- `election_district` (array<string>): House district of the office sought, if applicable.
- `election_party` (array<string>): Party, if applicable.
- `election_state` (array<string>): State or territory of the office sought.
- `election_type_id` (array<string>): Election type id
- `election_year` (array<string>): Year of election
- `max_create_date` (string): The maximum date this record was added to the system.(MM/DD/YYYY or YYYY-MM-DD)
- `max_election_date` (string): The maximum date of election.
- `max_primary_general_date` (string): The maximum date of primary or general election.(MM/DD/YYYY or YYYY-MM-DD)
- `max_update_date` (string): The maximum date this record was last updated.(MM/DD/YYYY or YYYY-MM-DD)
- `min_create_date` (string): The minimum date this record was added to the system.(MM/DD/YYYY or YYYY-MM-DD)
- `min_election_date` (string): The minimum date of election.
- `min_primary_general_date` (string): The minimum date of primary or general election.(MM/DD/YYYY or YYYY-MM-DD)
- `min_update_date` (string): The minimum date this record was last updated.(MM/DD/YYYY or YYYY-MM-DD)
- `office_sought` (array<string>, one of: H, S, P): House, Senate or presidential office.

### GET /reporting-dates/
FEC election dates since 1995.

**Query parameters:**
- `max_create_date` (string): The maximum date this record was added to the system.(MM/DD/YYYY or YYYY-MM-DD)
- `max_due_date` (string): The maximum date the report is due.(MM/DD/YYYY or YYYY-MM-DD)
- `max_update_date` (string): The maximum date this record was last updated.(MM/DD/YYYY or YYYY-MM-DD)
- `min_create_date` (string): The minimum date this record was added to the system.(MM/DD/YYYY or YYYY-MM-DD)
- `min_due_date` (string): The minimum date the report is due.(MM/DD/YYYY or YYYY-MM-DD)
- `min_update_date` (string): The minimum date this record was last updated.(MM/DD/YYYY or YYYY-MM-DD)
- `report_type` (array<string>): Name of report where the underlying data comes from: - 10D Pre-Election - 10G Pre-General - 10P Pre-Primary - 10R Pre-Run-Off - 10S Pre-Spe…
- `report_year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.
