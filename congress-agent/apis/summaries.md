# Summaries API

Endpoints for CRS-written bill summaries.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`, `sort` (e.g. `updateDate+desc`)
- **`billType` values:** `hr`, `s`, `hjres`, `sjres`, `hconres`, `sconres`, `hres`, `sres`

## Endpoints

### GET /summaries
Returns a list of bill summaries sorted by date of last update.

### GET /summaries/{congress}
Summaries filtered by Congress.
- Path: `congress`

### GET /summaries/{congress}/{billType}
Summaries filtered by Congress and bill type.
- Path: `congress`, `billType`
