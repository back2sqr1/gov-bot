---
name: house-communication
description: Communications received by the House (executive communications, presidential messages, petitions, memorials).
---

# House Communication API

Endpoints for communications received by the House of Representatives.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)
- **`communicationType` values:** `ec` (executive communication), `pm` (presidential message), `pt` (petition), `ml` (memorial)

## Endpoints

### GET /house-communication
Returns a list of House communications.

### GET /house-communication/{congress}
House communications filtered by Congress.
- Path: `congress`

### GET /house-communication/{congress}/{communicationType}
House communications filtered by Congress and type.
- Path: `congress`, `communicationType`

### GET /house-communication/{congress}/{communicationType}/{communicationNumber}
Detail for a specific House communication.
- Path: `congress`, `communicationType`, `communicationNumber`
