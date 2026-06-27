---
name: hearing
description: Printed congressional hearings.
---

# Hearing API

Endpoints for printed congressional hearings.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)
- **`chamber` values:** `house`, `senate`, `nochamber`

## Endpoints

### GET /hearing
Returns a list of hearings.

### GET /hearing/{congress}
Hearings filtered by Congress.
- Path: `congress`

### GET /hearing/{congress}/{chamber}
Hearings filtered by Congress and chamber.
- Path: `congress`, `chamber`

### GET /hearing/{congress}/{chamber}/{jacketNumber}
Detail for a specific hearing.
- Path: `congress`, `chamber`, `jacketNumber` (typically five digits)
