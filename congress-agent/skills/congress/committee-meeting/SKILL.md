---
name: committee-meeting
description: Scheduled committee meetings and meeting details.
---

# Committee Meeting API

Endpoints for scheduled committee meetings.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)
- **`chamber` values:** `house`, `senate`, `nochamber`

## Endpoints

### GET /committee-meeting
Returns a list of committee meetings.

### GET /committee-meeting/{congress}
Committee meetings filtered by Congress.
- Path: `congress`

### GET /committee-meeting/{congress}/{chamber}
Committee meetings filtered by Congress and chamber.
- Path: `congress`, `chamber`

### GET /committee-meeting/{congress}/{chamber}/{eventId}
Detail for a specific committee meeting.
- Path: `congress`, `chamber`, `eventId` (e.g. `115538`)
