# Bound Congressional Record API

Endpoints for the bound Congressional Record (by date).

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)

## Endpoints

### GET /bound-congressional-record
Returns a list of bound Congressional Record issues.

### GET /bound-congressional-record/{year}
Bound Congressional Record filtered by year.
- Path: `year`

### GET /bound-congressional-record/{year}/{month}
Bound Congressional Record filtered by year and month.
- Path: `year`, `month`

### GET /bound-congressional-record/{year}/{month}/{day}
Bound Congressional Record filtered by specific date.
- Path: `year`, `month`, `day`
