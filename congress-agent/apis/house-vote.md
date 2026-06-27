# House Roll Call Vote API

Endpoints for House of Representatives roll call votes. (Beta / may change.)

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)
- **`sessionNumber` values:** `1` or `2`

## Endpoints

### GET /house-vote/{congress}/{sessionNumber}
All House roll call votes for a Congress and session.
- Path: `congress`, `sessionNumber`

### GET /house-vote/{congress}/{sessionNumber}/{rollCallNumber}
Detail for a specific House roll call vote (type, result, party totals).
- Path: `congress`, `sessionNumber`, `rollCallNumber`

### GET /house-vote/{congress}/{sessionNumber}/{rollCallNumber}/members
How individual members voted on a specific roll call vote.
- Path: `congress`, `sessionNumber`, `rollCallNumber`
