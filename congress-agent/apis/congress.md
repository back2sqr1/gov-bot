# Congress API

Endpoints for Congresses and their sessions.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)

## Endpoints

### GET /congress
Returns a list of Congresses and congressional sessions.

### GET /congress/{congress}
Detail for a specific Congress, including its sessions, name, and years.
- Path: `congress` (e.g. `116`)

### GET /congress/current
Detail for the current Congress.
