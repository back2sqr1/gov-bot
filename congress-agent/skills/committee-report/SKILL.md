---
name: committee-report
description: Committee reports (HRPT, SRPT, ERPT) and their text.
---

# Committee Report API

Endpoints for committee reports.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `conference` (true|false), `fromDateTime`, `toDateTime`
- **`reportType` values:** `hrpt`, `srpt`, `erpt`

## Endpoints

### GET /committee-report
Returns a list of committee reports.

### GET /committee-report/{congress}
Committee reports filtered by Congress.
- Path: `congress`

### GET /committee-report/{congress}/{reportType}
Committee reports filtered by Congress and report type.
- Path: `congress`, `reportType`

### GET /committee-report/{congress}/{reportType}/{reportNumber}
Detail for a specific committee report.
- Path: `congress`, `reportType`, `reportNumber`

### GET /committee-report/{congress}/{reportType}/{reportNumber}/text
Text versions and formats of a committee report.
- Path: `congress`, `reportType`, `reportNumber`
