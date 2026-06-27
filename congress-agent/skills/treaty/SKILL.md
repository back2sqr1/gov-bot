---
name: treaty
description: Treaties submitted to the Senate: actions, committees, and parts.
---

# Treaty API

Endpoints for treaties submitted to the Senate.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format`, `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`
- **`suffix`:** treaty part identifier (`A`, `B`, `C`, ...) for partitioned treaties

## Endpoints

### GET /treaty
Returns a list of treaties sorted by date of last update.

### GET /treaty/{congress}
Treaties filtered by Congress.
- Path: `congress`

### GET /treaty/{congress}/{number}
Detail for a specific treaty.
- Path: `congress`, `number`

### GET /treaty/{congress}/{number}/{suffix}
Detail for a specific partitioned treaty.
- Path: `congress`, `number`, `suffix`

### GET /treaty/{congress}/{number}/actions
Actions taken on a treaty.
- Path: `congress`, `number`

### GET /treaty/{congress}/{number}/{suffix}/actions
Actions taken on a partitioned treaty.
- Path: `congress`, `number`, `suffix`

### GET /treaty/{congress}/{number}/committees
Committees associated with a treaty.
- Path: `congress`, `number`
