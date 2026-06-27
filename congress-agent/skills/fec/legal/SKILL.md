---
name: legal
description: Explore relevant statutes, regulations and Commission actions.
---

# Legal API

Explore relevant statutes, regulations and Commission actions.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /legal/docs/{doc_type}/{no}
Search legal documents by type and number

**Path parameters:**
- `doc_type` (string, required, one of: statutes, admin_fines, adrs, advisory_opinions, murs): Choose a legal document type: advisory_opinions, murs, admin_fines, statutes, or adrs
- `no` (string, required): Document number to fetch

### GET /legal/search/
Search legal documents by document type, or across all document types using keywords, parameter values and ranges. This endpoint uses opensearch-dsl pagination.For pagination, use both `from_hit` and `hits_returned` parameters. `from_hit` defines the offset from the first result you want to fetch. `hits_returned` allows you to configure the maximum results to be returned. By default `from_hit` =…

**Query parameters:**
- `af_committee_id` (string): Admin fine committee ID
- `af_fd_fine_amount` (integer): Final Determination fine amount
- `af_max_fd_date` (string): The latest Final Determination date
- `af_max_rtb_date` (string): The latest Reason to Believe date
- `af_min_fd_date` (string): The earliest Final Determination date
- `af_min_rtb_date` (string): The earliest Reason to Believe date
- `af_name` (array<string>): Admin fine committee name
- `af_report_year` (string): Admin fine report year
- `af_rtb_fine_amount` (integer): Reason to Believe fine amount
- `ao_citation_require_all` (boolean): Require all citations to be in document (default behavior is any)
- `ao_commenter` (string): Name of commenter
- `ao_doc_category_id` (array<string>, one of: F, V, D, R, W, C, S): Category of the document F - Final Opinion V - Votes D - Draft Documents R - AO Request, Supplemental Material, and Extensions of Time W -…
- `ao_is_pending` (boolean): AO is pending
- `ao_max_document_date` (string): Selects all advisory opinion documents dated on or before this date. Date must be formatted as MM/DD/YYYY or YYYY-MM-DD."
- `ao_max_issue_date` (string): Latest issue date of advisory opinion
- `ao_max_request_date` (string): Latest request date of advisory opinion
- `ao_min_document_date` (string): Selects all advisory opinion documents dated on or after this date. Date must be formatted as MM/DD/YYYY or YYYY-MM-DD."
- `ao_min_issue_date` (string): Earliest issue date of advisory opinion
- `ao_min_request_date` (string): Earliest request date of advisory opinion
- `ao_name` (array<string>): Advisory opinion name
- `ao_no` (array<string>): Advisory opinion number
- `ao_regulatory_citation` (array<string>): Regulatory citations
- `ao_representative` (string): Name of representative
- `ao_requestor` (string): The requestor of the advisory opinion
- `ao_requestor_type` (array<string>): Code of the advisory opinion requestor type. Select one or more codes to filter by advisory opinion requestor type: - 1 - Federal candidate…
- `ao_status` (string): Status of AO (pending, withdrawn, or final)
- `ao_statutory_citation` (array<string>): Statutory citations
- `ao_year` (integer): Advisory opinion year
- `case_citation_require_all` (boolean): Require all citations to be in document (default behavior is any)
- `case_doc_category_id` (array<string>): Select one or more case document category id to filter by corresponding case document category: - 1 - Conciliation and Settlement Agreement…
- `case_election_cycles` (integer): Cases election cycles
- `case_max_close_date` (string): The latest date closed of case
- `case_max_document_date` (string): Selects all case documents dated on or before this date. Date must be formatted as MM/DD/YYYY or YYYY-MM-DD."
- `case_max_open_date` (string): The latest date opened of case
- `case_max_penalty_amount` (string): Show cases with a penalty less than this amount
- `case_min_close_date` (string): The earliest date closed of case
- `case_min_document_date` (string): Selects all case documents dated on or after this date. Date must be formatted as MM/DD/YYYY or YYYY-MM-DD."
- `case_min_open_date` (string): The earliest date opened of case
- `case_min_penalty_amount` (string): Show cases with a penalty greater than this amount
- `case_no` (array<string>): Enforcement matter case number
- `case_regulatory_citation` (array<string>): Regulatory citations
- `case_respondents` (string): Cases respondents
- `case_statutory_citation` (array<string>): Statutory citations
- `filename` (string): Search documents by file name
- `from_hit` (integer): Get results starting from this index
- `hits_returned` (integer): Number of results to return. The default value is 20, with a maximum limit of 200 results per page
- `max_gaps` (integer): The maximum number of positions allowed between terms specified in `q_proximity`
- `mur_disposition_category_id` (array<string>): Select one or more MUR disposition category id to filter by corresponding MUR disposition category: - 1 - Conciliation: Pre Probable Cause…
- `mur_type` (string, one of: archived, current): Type of MUR : current or archived
- `primary_subject_id` (array<string>): Primary Subject Description: - 1 - Allocation - 2 - Committees - 3 - Contributions - 4 - Disclaimer - 5 - Disbursements - 6 - Electioneerin…
- `proximity_filter` (string, one of: after, before): Adds additional filters to the proximity search that provides options to specify positional constraints
- `proximity_filter_term` (string): Specifies the term to which the `proximity_filter` option applies to and defines what must appear in relation to the `q_proximity` phrase
- `proximity_preserve_order` (boolean): When set to true, maintains the original order of phrases in `q_proximity`.
- `q` (string): Search field to find documents containing a word or phrase in their text.
- `q_exclude` (string): Exclude documents containing this term
- `q_proximity` (array<string>): This search identifies documents where the specified phrases appear near each other. The field supports both a single phrase or multiple ph…
- `secondary_subject_id` (array<string>): Secondary Subject Description: - 1 - Candidate - 2 - Multi-candidate - 3 - Non-party - 4 - PAC - 5 - Party - 6 - Political - 7 - Presidenti…
- `type` (string, one of: admin_fines, adrs, advisory_opinions, murs, statutes): Choose a legal document type: advisory_opinions, murs, admin_fines, statutes, or adrs

### GET /rulemaking/search/
The Searchable Electronic Rulemaking System (SERS) lets you search all public documents associated with Federal Election Commission rulemakings (REGs), including draft Federal Register publications, open meeting agendas, comments submitted by the public, and hearing transcripts.

**Query parameters:**
- `doc_category_id` (array<string>, one of: 1, 2, 3, 4, 5, 6, 7, 8): Category of the rulemaking document - 1 - Open Meeting - 2 - Hearing - 3 - Agenda Document - 4 - Federal Register Document - 5 - Comments a…
- `doc_id` (integer): Filter rulemakings by a specific document ID (`doc_id`). Returns only rulemakings that contain a document matching the given ID.
- `entity_name` (string): Name of the entity related a specific rulemaking
- `entity_role_type` (array<string>, one of: 1, 2, 3, 4, 5): An "entity" is any individual or group that plays one of the following roles with respect to a REG. The different entity roles are: - 1 - P…
- `filename` (string): Search documents by file name
- `from_hit` (integer): Get results starting from this index
- `hits_returned` (integer): Number of results to return. The default value is 30, with a maximum limit of 200 results per page
- `is_key_document` (boolean): When set to true, only rulemakings with at least one key document are returned
- `is_open_for_comment` (boolean): When set to true, this flag returns rulemakings that are currently open for comment.
- `max_federal_registry_publish_date` (string): Search for documents associated with a REG where the Federal Register published a REG document approved by the Commission on or before this…
- `max_gaps` (integer): The maximum number of positions allowed between terms specified in `q_proximity`
- `max_hearing_date` (string): Search for documents associated with a REG where the Commission held a hearing on or before this date. Date must be formatted as MM/DD/YYYY…
- `max_vote_date` (string): Search for documents associated with a REG where the Commission voted on an agenda document on or after this date. Date must be formatted a…
- `min_federal_registry_publish_date` (string): Search for documents associated with a REG where the Federal Register published a REG document approved by the Commission on or after this…
- `min_hearing_date` (string): Search for documents associated with a REG where the Commission held a hearing on or after this date. Date must be formatted as MM/DD/YYYY…
- `min_vote_date` (string): Search for documents associated with a REG where the Commission voted on an agenda document on or after this date. Date must be formatted a…
- `proximity_filter` (string, one of: after, before): Adds additional filters to the proximity search that provides options to specify positional constraints
- `proximity_filter_term` (string): Specifies the term to which the `proximity_filter` option applies to and defines what must appear in relation to the `q_proximity` phrase
- `proximity_preserve_order` (boolean): When set to true, maintains the original order of phrases in `q_proximity`.
- `q` (string): Search field to find documents containing a word or phrase in their text.
- `q_exclude` (string): Exclude documents containing this term
- `q_proximity` (array<string>): This search identifies documents where the specified phrases appear near each other. The field supports both a single phrase or multiple ph…
- `rm_name` (array<string>): Search REG Name field to retrieve REG documents with specific words in their names.
- `rm_no` (array<string>): Search a REG number to go directly to the REG and all associated documents. REG numbers are listed in a YYYY-PP format
- `rm_year` (integer): Search by REG documents by the year in which a rulemaking began
