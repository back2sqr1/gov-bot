# Member API

Endpoints for members of Congress and their legislation.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `currentMember` (true|false), `fromDateTime`, `toDateTime`

## Endpoints

### GET /member
Returns a list of congressional members.

### GET /member/{bioguideId}
Detail for a specific member.
- Path: `bioguideId` (e.g. `L000174`)

### GET /member/{bioguideId}/sponsored-legislation
Bills and resolutions sponsored by a member.
- Path: `bioguideId`

### GET /member/{bioguideId}/cosponsored-legislation
Bills and resolutions cosponsored by a member.
- Path: `bioguideId`

### GET /member/congress/{congress}
Members of a specific Congress.
- Path: `congress`
- Query: `currentMember`

### GET /member/{stateCode}
Members filtered by state.
- Path: `stateCode` (two-letter, e.g. `MI`)
- Query: `currentMember`

### GET /member/{stateCode}/{district}
Members filtered by state and district.
- Path: `stateCode`, `district`
- Query: `currentMember`

### GET /member/congress/{congress}/{stateCode}/{district}
Members filtered by Congress, state, and district.
- Path: `congress`, `stateCode`, `district`
- Query: `currentMember`
