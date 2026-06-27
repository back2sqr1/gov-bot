---
name: receipts
description: This collection of endpoints includes Schedule A records reported by a committee.
---

# Receipts API

This collection of endpoints includes Schedule A records reported by a committee. Schedule A records describe itemized receipts, including contributions from individuals. If you are interested in contributions from individuals, use the /schedules/schedule_a/ endpoint. For a more complete description of all Schedule A records visit [About receipts data](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/about-receipts-data/). If you are interested in our "is_individual" methodology visit our [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology/). Schedule A is also available as a database dump file that is updated weekly on Sunday. The database dump files are here: https://www.fec.gov/files/bulk-downloads/index.html?prefix=bulk-downloads/data-dump/schedules/. The instructions are here: https://www.fec.gov/files//bulk-downloads/data-dump/schedules/README.txt. We cannot provide help with restoring the database dump files, but you can refer to this community led [group](https://groups.google.com/forum/#!forum/fec-data) for discussion.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /schedules/schedule_a/
This description is for both ​`/schedules​/schedule_a​/` and ​ `/schedules​/schedule_a​/{sub_id}​/`. This endpoint provides itemized receipts. Schedule A records describe itemized receipts, including contributions from individuals. If you are interested in contributions from an individual, use the `/schedules/schedule_a/` endpoint. For a more complete description of all Schedule A records visit […

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `contributor_city` (array<string>): City of contributor
- `contributor_employer` (array<string>): Employer of contributor, filers need to make an effort to gather this information
- `contributor_id` (array<string>): The FEC identifier should be represented here if the contributor is registered with the FEC.
- `contributor_name` (array<string>): Name of contributor
- `contributor_occupation` (array<string>): Occupation of contributor, filers need to make an effort to gather this information
- `contributor_state` (array<string>): State of contributor. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and…
- `contributor_type` (array<string>, one of: individual, committee): Filters individual or committee contributions based on line number
- `contributor_zip` (array<string>): Zip code of contributor
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `is_individual` (boolean): Restrict to non-earmarked individual contributions where memo code is true. Filtering individuals is useful to make sure contributions are…
- `last_contribution_receipt_amount` (number): When sorting by `contribution_receipt_amount`, this is populated with the contribution_receipt_amount` of the last result. However, you wil…
- `last_contribution_receipt_date` (string): When sorting by `contribution_receipt_date`, this is populated with the contribution_receipt_date` of the last result. However, you will ne…
- `last_index` (integer): Index of last result from previous page
- `line_number` (string): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `max_load_date` (string): Maximum load date
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `min_load_date` (string): Minimum load date
- `recipient_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `recipient_committee_org_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `recipient_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…

### GET /schedules/schedule_a/by_employer/
This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s employer name. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `employer` (array<string>): Employer of contributor as reported on the committee's filing

### GET /schedules/schedule_a/by_occupation/
This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s occupation. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `occupation` (array<string>): Occupation of contributor as reported on the committee's filing

### GET /schedules/schedule_a/by_size/
This endpoint provides individual contributions received by a committee, aggregated by size: ``` - $200 and under - $200.01 - $499.99 - $500 - $999.99 - $1000 - $1999.99 - $2000 + ``` The $200.00 and under category includes contributions of $200 or less combined with unitemized individual contributions.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `size` (array<integer>, one of: 0, 200, 500, 1000, 2000): The total all contributions in the following ranges: ``` -0 $200 and under -200 $200.01 - $499.99 -500 $500 - $999.99 -1000 $1000 - $1999.9…

### GET /schedules/schedule_a/by_size/by_candidate/
This endpoint provides itemized individual contributions received by a committee, aggregated by size of contribution and candidate. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `candidate_id` (array<string>, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>, required): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /schedules/schedule_a/by_state/
This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s state. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `hide_null` (boolean): Exclude values with missing state
- `state` (array<string>): State of contributor

### GET /schedules/schedule_a/by_state/by_candidate/
This endpoint provides itemized individual contributions received by a committee, aggregated by contributor’s state and candidate. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `candidate_id` (array<string>, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>, required): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /schedules/schedule_a/by_state/by_candidate/totals/
Itemized individual contributions aggregated by contributor’s state, candidate, committee type and cycle. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `candidate_id` (array<string>, required): A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separat…
- `cycle` (array<integer>, required): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `election_full` (boolean): `True` indicates that full election period of a candidate. `False` indicates that two year election cycle.

### GET /schedules/schedule_a/by_state/totals/
This endpoint provides itemized individual contributions received by a committee, aggregated by contributor’s state, committee type and cycle. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `state` (array<string>): US state or territory

### GET /schedules/schedule_a/by_zip/
This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s ZIP code. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `state` (array<string>): State of contributor
- `zip` (array<string>): Zip code of contributor

### GET /schedules/schedule_a/efile/
Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `contributor_city` (array<string>): City of contributor
- `contributor_employer` (array<string>): Employer of contributor, filers need to make an effort to gather this information
- `contributor_name` (array<string>): Name of contributor
- `contributor_occupation` (array<string>): Occupation of contributor, filers need to make an effort to gather this information
- `contributor_state` (array<string>): State of contributor
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported

### GET /schedules/schedule_a/{sub_id}/
This description is for both ​`/schedules​/schedule_a​/` and ​ `/schedules​/schedule_a​/{sub_id}​/`. This endpoint provides itemized receipts. Schedule A records describe itemized receipts, including contributions from individuals. If you are interested in contributions from an individual, use the `/schedules/schedule_a/` endpoint. For a more complete description of all Schedule A records visit […

**Path parameters:**
- `sub_id` (string, required)

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `contributor_city` (array<string>): City of contributor
- `contributor_employer` (array<string>): Employer of contributor, filers need to make an effort to gather this information
- `contributor_id` (array<string>): The FEC identifier should be represented here if the contributor is registered with the FEC.
- `contributor_name` (array<string>): Name of contributor
- `contributor_occupation` (array<string>): Occupation of contributor, filers need to make an effort to gather this information
- `contributor_state` (array<string>): State of contributor. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and…
- `contributor_type` (array<string>, one of: individual, committee): Filters individual or committee contributions based on line number
- `contributor_zip` (array<string>): Zip code of contributor
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `is_individual` (boolean): Restrict to non-earmarked individual contributions where memo code is true. Filtering individuals is useful to make sure contributions are…
- `last_contribution_receipt_amount` (number): When sorting by `contribution_receipt_amount`, this is populated with the contribution_receipt_amount` of the last result. However, you wil…
- `last_contribution_receipt_date` (string): When sorting by `contribution_receipt_date`, this is populated with the contribution_receipt_date` of the last result. However, you will ne…
- `last_index` (integer): Index of last result from previous page
- `line_number` (string): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `max_load_date` (string): Maximum load date
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `min_load_date` (string): Minimum load date
- `recipient_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `recipient_committee_org_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `recipient_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…

### GET /schedules/schedule_a_form5/
FEC FORM 5 Receipts REPORT OF INDEPENDENT EXPENDITURES MADE AND CONTRIBUTIONS RECEIVED To Be Used By Persons (Other than Political Committees)

**Query parameters:**
- `contributor_city` (array<string>): City of contributor
- `contributor_employer` (array<string>): Employer of contributor, filers need to make an effort to gather this information
- `contributor_name` (array<string>): Name of contributor
- `contributor_occupation` (array<string>): Occupation of contributor, filers need to make an effort to gather this information
- `contributor_state` (array<string>): State of contributor
- `contributor_type` (array<string>, one of: individual, committee): Filters individual or committee contributions based on line number
- `contributor_zip` (array<string>): Zip code of contributor
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `last_contribution_amount` (number): When sorting by `contribution_amount`, this is populated with the contribution_amount` of the last result. However, you will need to pass t…
- `last_contribution_receipt_date` (string): When sorting by `contribution_receipt_date`, this is populated with the contribution_receipt_date` of the last result. However, you will ne…
- `last_index` (integer): Index of last result from previous page
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `report_type` (array<string>): Name of report where the underlying data comes from: - 10D Pre-Election - 10G Pre-General - 10P Pre-Primary - 10R Pre-Run-Off - 10S Pre-Spe…
- `report_year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…
