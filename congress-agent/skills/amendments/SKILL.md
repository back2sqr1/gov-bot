---
name: amendments
description: Amendments to bills and to other amendments: actions, cosponsors, and text.
---

# Amendments API

Endpoints for amendments to bills and to other amendments.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`
- **`type` values:** `hamdt`, `samdt`, `suamdt`

## Endpoints

### GET /amendment
Returns a list of amendments sorted by date of latest action.

### GET /amendment/{congress}
Amendments filtered by Congress.
- Path: `congress`

### GET /amendment/{congress}/{type}
Amendments filtered by Congress and amendment type.
- Path: `congress`, `type`

### GET /amendment/{congress}/{type}/{number}
Detail for a specific amendment.
- Path: `congress`, `type`, `number`

### GET /amendment/{congress}/{type}/{number}/actions
Actions taken on an amendment.

### GET /amendment/{congress}/{type}/{number}/amendments
Amendments that modify the specified amendment.

### GET /amendment/{congress}/{type}/{number}/cosponsors
Cosponsors of an amendment (Senate amendments).

### GET /amendment/{congress}/{type}/{number}/text
Text versions of an amendment (Senate amendments and some House amendments, 117th Congress forward).
