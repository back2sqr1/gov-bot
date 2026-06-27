---
name: audit
description: The agency’s monitoring process may detect potential violations through a review of a committee’s reports or through a Commission audit.
---

# Audit API

The agency’s monitoring process may detect potential violations through a review of a committee’s reports or through a Commission audit. By law, all enforcement cases must remain confidential until they’re closed. The Commission is required by law to audit Presidential campaigns that accept public funds. In addition, the Commission audits a committee when it appears not to have met the threshold requirements for substantial compliance with the Federal Election Campaign Act. The audit determines whether the committee complied with limitations, prohibitions and disclosure requirements. These endpoints contain Final Audit Reports approved by the Commission since inception.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /audit-case/
This endpoint contains Final Audit Reports approved by the Commission since inception. The search can be based on information about the audited committee (Name, FEC ID Number, Type, Election Cycle) or the issues covered in the report.

**Query parameters:**
- `audit_case_id` (array<string>): Primary/foreign key for audit tables
- `audit_id` (array<integer>): The audit issue. Each subcategory has an unique ID
- `candidate_id` (array<string>): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `committee_designation` (string): Type of committee: - H or S - Congressional - P - Presidential - X or Y or Z - Party - N or Q - PAC - I - Independent expenditure - O - Sup…
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): Filter records to only those that are applicable to a given two-year period. This cycle follows the traditional House election cycle and su…
- `max_election_cycle` (integer): Filter records to only those that are applicable to a given two-year period. This cycle follows the traditional House election cycle and su…
- `min_election_cycle` (integer): Filter records to only those that are applicable to a given two-year period. This cycle follows the traditional House election cycle and su…
- `primary_category_id` (string): Audit category ID (table PK)
- `q` (array<string>): The name of the committee. If a committee changes its name, the most recent name will be shown. Committee names are not unique. Use committ…
- `qq` (array<string>): Name of candidate running for office
- `sub_category_id` (string): The finding id of an audit. Finding are a category of broader issues. Each category has an unique ID.

### GET /audit-category/
This lists the options for the categories and subcategories available in the /audit-search/ endpoint.

**Query parameters:**
- `primary_category_id` (array<string>): Audit category ID (table PK)
- `primary_category_name` (array<string>): Primary Audit Category - No Findings or Issues/Not a Committee - Net Outstanding Campaign/Convention Expenditures/Obligations - Payments/Di…

### GET /audit-primary-category/
This lists the options for the primary categories available in the /audit-search/ endpoint.

**Query parameters:**
- `primary_category_id` (array<string>): Audit category ID (table PK)
- `primary_category_name` (array<string>): Primary Audit Category - No Findings or Issues/Not a Committee - Net Outstanding Campaign/Convention Expenditures/Obligations - Payments/Di…

### GET /names/audit_candidates/
Search for candidates or committees by name. If you're looking for information on a particular person or group, using a name to find the `candidate_id` or `committee_id` on this endpoint can be a helpful first step.

**Query parameters:**
- `q` (array<string>, required): Name (candidate or committee) to search for

### GET /names/audit_committees/
Search for candidates or committees by name. If you're looking for information on a particular person or group, using a name to find the `candidate_id` or `committee_id` on this endpoint can be a helpful first step.

**Query parameters:**
- `q` (array<string>, required): Name (candidate or committee) to search for
