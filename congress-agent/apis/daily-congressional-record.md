# Daily Congressional Record API

Endpoints for the daily Congressional Record (by volume and issue).

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250)

## Endpoints

### GET /daily-congressional-record
Returns a list of daily Congressional Record issues.

### GET /daily-congressional-record/{volumeNumber}
Daily Congressional Record filtered by volume.
- Path: `volumeNumber`

### GET /daily-congressional-record/{volumeNumber}/{issueNumber}
A specific daily Congressional Record issue within a volume.
- Path: `volumeNumber`, `issueNumber`

### GET /daily-congressional-record/{volumeNumber}/{issueNumber}/articles
Articles within a specific daily Congressional Record issue.
- Path: `volumeNumber`, `issueNumber`
