---
name: committee-print
description: Committee prints and their text.
---

# Committee Print API

Endpoints for committee prints.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`
- **`chamber` values:** `house`, `senate`, `nochamber`

## Endpoints

### GET /committee-print
Returns a list of committee prints.

### GET /committee-print/{congress}
Committee prints filtered by Congress.
- Path: `congress`

### GET /committee-print/{congress}/{chamber}
Committee prints filtered by Congress and chamber.
- Path: `congress`, `chamber`

### GET /committee-print/{congress}/{chamber}/{jacketNumber}
Detail for a specific committee print.
- Path: `congress`, `chamber`, `jacketNumber` (five-digit identifier)

### GET /committee-print/{congress}/{chamber}/{jacketNumber}/text
Text formats for a committee print (PDF, formatted text, XML, HTML).
- Path: `congress`, `chamber`, `jacketNumber`
