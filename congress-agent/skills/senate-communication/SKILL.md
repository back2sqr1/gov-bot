---
name: senate-communication
description: Communications received by the Senate.
---

# Senate Communication API

Endpoints for communications received by the Senate.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)
- **`communicationType` values:** `ec` (executive communication), `pm` (presidential message), `pom` (petition or memorial)

## Endpoints

### GET /senate-communication
Returns a list of Senate communications.

### GET /senate-communication/{congress}
Senate communications filtered by Congress.
- Path: `congress`

### GET /senate-communication/{congress}/{communicationType}
Senate communications filtered by Congress and type.
- Path: `congress`, `communicationType`

### GET /senate-communication/{congress}/{communicationType}/{communicationNumber}
Detail for a specific Senate communication.
- Path: `congress`, `communicationType`, `communicationNumber`
