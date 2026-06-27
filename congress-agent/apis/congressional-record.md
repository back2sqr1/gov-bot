# Congressional Record API

Endpoints for the Congressional Record.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)

## Endpoints

### GET /congressional-record
Returns a list of Congressional Record issues, filterable by date.
- Query: `y` (year, e.g. `2022`), `m` (month, e.g. `6`), `d` (day, e.g. `28`)
