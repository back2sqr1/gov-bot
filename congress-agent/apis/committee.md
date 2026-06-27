# Committee API

Endpoints for congressional committees and subcommittees, and their associated items.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)
- **`chamber` values:** `house`, `senate`, `joint`

## Endpoints

### GET /committee
Returns a list of congressional committees.

### GET /committee/{chamber}
Committees filtered by chamber.
- Path: `chamber`

### GET /committee/{congress}
Committees filtered by Congress.
- Path: `congress`

### GET /committee/{congress}/{chamber}
Committees filtered by Congress and chamber.
- Path: `congress`, `chamber`

### GET /committee/{chamber}/{committeeCode}
Detail for a specific committee or subcommittee.
- Path: `chamber`, `committeeCode` (system code, e.g. `hspw00`)

### GET /committee/{chamber}/{committeeCode}/bills
Bills and resolutions associated with a committee.
- Path: `chamber`, `committeeCode`

### GET /committee/{chamber}/{committeeCode}/reports
Committee reports issued by a committee.
- Path: `chamber`, `committeeCode`

### GET /committee/{chamber}/{committeeCode}/nominations
Nominations associated with a committee (Senate).
- Path: `chamber`, `committeeCode`

### GET /committee/{chamber}/{committeeCode}/house-communication
House communications associated with a committee.
- Path: `chamber`, `committeeCode`

### GET /committee/{chamber}/{committeeCode}/senate-communication
Senate communications associated with a committee.
- Path: `chamber`, `committeeCode`
