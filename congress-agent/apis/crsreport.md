# CRS Report API

Endpoints for Congressional Research Service (CRS) reports.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`

## Endpoints

### GET /crsreport
Returns a list of CRS reports.

### GET /crsreport/{reportNumber}
Detail for a specific CRS report.
- Path: `reportNumber` (e.g. `R47175`)
