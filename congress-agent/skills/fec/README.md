# OpenFEC Skills

One skill per OpenFEC API group, in the same format as the Congress.gov skills
(`../congress/`): YAML frontmatter (`name`, `description`) for orchestrator
selection, then a body documenting the base URL, auth, common params, and every
endpoint in that group with its path/query parameters. The registry keys these
as `fec/<group>` (e.g. `fec/candidate`) so they never collide with same-named
Congress.gov groups, and the orchestrator can mix both sources in one answer.

These are generated from the live OpenFEC OpenAPI (swagger) spec by
`../../scripts/generate_fec_skills.py`. The 20 groups (swagger tags) are:

`audit`, `candidate`, `committee`, `communication-cost`, `dates`, `debts`,
`disbursements`, `efiling`, `electioneering`, `filer-resources`, `filings`,
`financial`, `independent-expenditures`, `legal`, `loans`,
`national-party-accounts`, `party-coordinated-expenditures`, `presidential`,
`receipts`, `search`.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** `?api_key=YOUR_KEY` (or `X-Api-Key` header). Free key:
  https://api.open.fec.gov/developers/ — `DEMO_KEY` works for light testing
  (40 calls/hour, shared).

## Regenerate

```bash
python scripts/generate_fec_skills.py
# offline, from a saved spec:
FEC_SWAGGER_FILE=/path/to/swagger.json python scripts/generate_fec_skills.py
```
