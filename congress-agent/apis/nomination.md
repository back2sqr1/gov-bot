# Nomination API

Endpoints for presidential nominations to the Senate.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`

## Endpoints

### GET /nomination
Returns a list of nominations sorted by date received from the President.

### GET /nomination/{congress}
Nominations filtered by Congress.
- Path: `congress`

### GET /nomination/{congress}/{nominationNumber}
Detail for a specific nomination.
- Path: `congress`, `nominationNumber`

### GET /nomination/{congress}/{nominationNumber}/{ordinal}
Nominees within a specific nomination (partitioned nominations).
- Path: `congress`, `nominationNumber`, `ordinal`

### GET /nomination/{congress}/{nominationNumber}/actions
Actions taken on a nomination.
- Path: `congress`, `nominationNumber`

### GET /nomination/{congress}/{nominationNumber}/committees
Committees associated with a nomination.
- Path: `congress`, `nominationNumber`

### GET /nomination/{congress}/{nominationNumber}/hearings
Printed hearings associated with a nomination.
- Path: `congress`, `nominationNumber`
