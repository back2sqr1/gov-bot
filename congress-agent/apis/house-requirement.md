# House Requirement API

Endpoints for House reporting requirements and their matching communications.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)

## Endpoints

### GET /house-requirement
Returns a list of House requirements.

### GET /house-requirement/{requirementNumber}
Detail for a specific House requirement.
- Path: `requirementNumber` (e.g. `12478`)

### GET /house-requirement/{requirementNumber}/matching-communications
House communications that match a specific requirement.
- Path: `requirementNumber`
