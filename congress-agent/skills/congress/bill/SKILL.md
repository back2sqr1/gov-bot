---
name: bill
description: Bills, resolutions, and enacted laws: actions, cosponsors, committees, text, summaries, titles, subjects, related bills, and amendments.
---

# Bill API

Endpoints for bills, resolutions, and enacted laws from Congress.gov.

- **Base URL:** `https://api.congress.gov/v3`
- **Auth:** every request requires `?api_key=YOUR_KEY`
- **Common query params:** `format` (json|xml), `offset`, `limit` (max 250), `fromDateTime`, `toDateTime`, `sort` (e.g. `updateDate+desc`)
- **`billType` values:** `hr`, `s`, `hjres`, `sjres`, `hconres`, `sconres`, `hres`, `sres`
- **`lawType` values:** `pub` (public law), `priv` (private law)

## Endpoints

### GET /bill
Returns a list of bills sorted by date of latest action.

### GET /bill/{congress}
Bills filtered by Congress (e.g. `117`).
- Path: `congress`

### GET /bill/{congress}/{billType}
Bills filtered by Congress and bill type.
- Path: `congress`, `billType`

### GET /bill/{congress}/{billType}/{number}
Detail for a specific bill or resolution.
- Path: `congress`, `billType`, `number`

### GET /bill/{congress}/{billType}/{number}/actions
Legislative actions on a bill.

### GET /bill/{congress}/{billType}/{number}/amendments
Amendments to a bill.

### GET /bill/{congress}/{billType}/{number}/committees
Committees associated with a bill.

### GET /bill/{congress}/{billType}/{number}/cosponsors
Cosponsors of a bill.

### GET /bill/{congress}/{billType}/{number}/relatedbills
Bills related to the specified bill.

### GET /bill/{congress}/{billType}/{number}/subjects
Legislative subject and policy area terms.

### GET /bill/{congress}/{billType}/{number}/summaries
CRS-written summaries for a bill.

### GET /bill/{congress}/{billType}/{number}/text
Text versions of a bill in available formats.

### GET /bill/{congress}/{billType}/{number}/titles
Official, short, and popular titles.

## Law Endpoints

### GET /law/{congress}
Laws (public and private) for a Congress.
- Path: `congress`

### GET /law/{congress}/{lawType}
Laws filtered by Congress and law type.
- Path: `congress`, `lawType`

### GET /law/{congress}/{lawType}/{number}
A specific law by Congress, type, and number.
- Path: `congress`, `lawType`, `number`
