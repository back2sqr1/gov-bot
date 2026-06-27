---
name: disbursements
description: Schedule B filings describe itemized disbursements.
---

# Disbursements API

Schedule B filings describe itemized disbursements. This data explains how committees and other filers spend their money. These figures are reported as part of forms F3, F3X and F3P.

- **Base URL:** `https://api.open.fec.gov/v1`
- **Auth:** every request requires an API key, sent either as the `?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).
- **Common query params (most list endpoints):** `page`, `per_page` (max 100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses are JSON with `results` plus a `pagination` block.

## Endpoints

### GET /schedules/schedule_b/
Schedule B filings describe itemized disbursements. This data explains how committees and other filers spend their money. These figures are reported as part of forms F3, F3X and F3P. The data are divided in two-year periods, called `two_year_transaction_period`, which is derived from the `report_year` submitted of the corresponding form. If no value is supplied, the results will default to the mo…

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `disbursement_description` (array<string>): Description of disbursement
- `disbursement_purpose_category` (array<string>, one of: ADMINISTRATIVE, ADVERTISING, CONTRIBUTIONS, EVENTS, FUNDRAISING, LOAN-REPAYMENTS, MATERIALS, OTHER, POLLING, REFUNDS, TRANSFERS, TRAVEL): Disbursement purpose category
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `last_disbursement_amount` (number): When sorting by `disbursement_amount`, this is populated with the `disbursement_amount` of the last result. However, you will need to pass…
- `last_disbursement_date` (string): When sorting by `disbursement_date`, this is populated with the `disbursement_date` of the last result. However, you will need to pass the…
- `last_index` (integer): Index of last result from previous page
- `line_number` (string): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `recipient_city` (array<string>): City of recipient
- `recipient_committee_id` (array<string>): The FEC identifier should be represented here if the contributor is registered with the FEC.
- `recipient_name` (array<string>): Name of the entity receiving the disbursement
- `recipient_state` (array<string>): State of recipient. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and a…
- `spender_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `spender_committee_org_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `spender_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…

### GET /schedules/schedule_b/by_purpose/
Schedule B disbursements aggregated by disbursement purpose category. To avoid double counting, memoed items are not included. Purpose is a combination of transaction codes, category codes and disbursement description. Inspect the `disbursement_purpose` sql function within the migrations for more details.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `purpose` (array<string>, one of: ADMINISTRATIVE, ADVERTISING, CONTRIBUTIONS, EVENTS, FUNDRAISING, LOAN-REPAYMENTS, MATERIALS, OTHER, POLLING, REFUNDS, TRANSFERS, TRAVEL): Disbursement purpose category

### GET /schedules/schedule_b/by_recipient/
Schedule B disbursements aggregated by recipient name. To avoid double counting, memoed items are not included.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `recipient_name` (array<string>): Name of the entity receiving the disbursement

### GET /schedules/schedule_b/by_recipient_id/
Schedule B disbursements aggregated by recipient committee ID, if applicable. To avoid double counting, memoed items are not included.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `recipient_id` (array<string>): The FEC identifier should be represented here if the entity receiving the disbursement is registered with the FEC.

### GET /schedules/schedule_b/efile/
Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `disbursement_description` (array<string>): Description of disbursement
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): When sorting by `disbursement_date`, this is populated with the `disbursement_date` of the last result. However, you will need to pass the…
- `min_amount` (number): Filter for all amounts less than a value.
- `min_date` (string): When sorting by `disbursement_date`, this is populated with the `disbursement_date` of the last result. However, you will need to pass the…
- `recipient_city` (array<string>): City of recipient
- `recipient_state` (array<string>): State of recipient

### GET /schedules/schedule_b/{sub_id}/
Schedule B filings describe itemized disbursements. This data explains how committees and other filers spend their money. These figures are reported as part of forms F3, F3X and F3P. The data are divided in two-year periods, called `two_year_transaction_period`, which is derived from the `report_year` submitted of the corresponding form. If no value is supplied, the results will default to the mo…

**Path parameters:**
- `sub_id` (string, required)

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `disbursement_description` (array<string>): Description of disbursement
- `disbursement_purpose_category` (array<string>, one of: ADMINISTRATIVE, ADVERTISING, CONTRIBUTIONS, EVENTS, FUNDRAISING, LOAN-REPAYMENTS, MATERIALS, OTHER, POLLING, REFUNDS, TRANSFERS, TRAVEL): Disbursement purpose category
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `last_disbursement_amount` (number): When sorting by `disbursement_amount`, this is populated with the `disbursement_amount` of the last result. However, you will need to pass…
- `last_disbursement_date` (string): When sorting by `disbursement_date`, this is populated with the `disbursement_date` of the last result. However, you will need to pass the…
- `last_index` (integer): Index of last result from previous page
- `line_number` (string): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): The latest date used to filter reported activity. Only records with an applicable reporting date before this date are returned.
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): The earliest date used to filter reported activity. Only records with an applicable reporting date after this date are returned.
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `recipient_city` (array<string>): City of recipient
- `recipient_committee_id` (array<string>): The FEC identifier should be represented here if the contributor is registered with the FEC.
- `recipient_name` (array<string>): Name of the entity receiving the disbursement
- `recipient_state` (array<string>): State of recipient. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other` for foreign countries and a…
- `spender_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `spender_committee_org_type` (array<string>, one of: C, L, M, T, V, W, H, I): The one-letter code for the kind for organization: - C corporation - L labor organization - M membership organization - T trade association…
- `spender_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…
- `two_year_transaction_period` (array<integer>): This is a two-year period that is derived from the year a transaction took place in the Itemized Schedule A and Schedule B tables. In cases…

### GET /schedules/schedule_h4/
Schedule H4 filings describe disbursements for allocated federal/nonfederal activity. This data demonstrates how separate segregated funds, party committees and nonconnected committees that are active in both federal and nonfederal elections, and have established separate federal and nonfederal accounts, allocate their activity. These figures are reported on Form 3X. The data are divided in two-y…

**Query parameters:**
- `activity_or_event` (array<string>): Additional description of activity_or_event
- `administrative_activity_indicator` (array<string>): Activity or event: Administrative checkbox
- `administrative_voter_drive_activity_indicator` (array<string>): Activity or event: Admin/Voter Drive checkbox
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `cycle` (array<integer>): Filter records to only those that were applicable to a given two-year period.The cycle begins with an odd year and is named for its ending,…
- `direct_candidate_support_activity_indicator` (array<string>): Activity or event: Direct Candidate checkbox
- `exempt_activity_indicator` (array<string>): Activity or event: Exempt checkbox
- `form_line_number` (array<string>): Filter for form and line number using the following format: `FORM-LINENUMBER`. For example an argument such as `F3X-16` would filter down t…
- `fundraising_activity_indicator` (array<string>): Activity or event: Fundraising checkbox
- `general_voter_drive_activity_indicator` (array<string>): Activity or event: Voter Drive checkbox
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `last_disbursement_amount` (number): When sorting by `disbursement_amount`, this is populated with the `disbursement_amount` of the last result. However, you will need to pass…
- `last_disbursement_purpose` (array<string>): When sorting by `disbursement_purpose`, this is populated with the `disbursement_purpose`of the last result. However, you will need to pass…
- `last_event_purpose_date` (string): When sorting by `event_purpose_date`, this is populated with the `event_purpose_date` of the last result. However, you will need to pass th…
- `last_index` (integer): Index of last result from previous page
- `last_payee_name` (array<string>): When sorting by `payee_name`, this is populated with the `payee_name` of the last result. However, you will need to pass the index of that…
- `last_spender_committee_name` (array<string>): When sorting by `spender_committee_name`, this is populated with the `spender_committee_name` of the last result. However, you will need to…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): Maximum event_purpose_date
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): Minimum event_purpose_date
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `payee_city` (array<string>): City of the entity that received the payment
- `payee_state` (array<string>): State of the entity that received the payment. A valid two-letter U.S. state or territory code. Use `ZZ` for foreign countries, or `other`…
- `payee_zip` (array<string>): Zip of the entity that received the payment
- `public_comm_indicator` (array<string>): Activity or event: Public Comm (ref to party only) by PAC checkbox
- `q_disbursement_purpose` (array<string>): Purpose of the allocated disbursement
- `q_payee_name` (array<string>): Name of the entity that received the payment.
- `report_type` (array<string>): Name of report where the underlying data comes from: - 10D Pre-Election - 10G Pre-General - 10P Pre-Primary - 10R Pre-Run-Off - 10S Pre-Spe…
- `report_year` (array<integer>): Forms with coverage date - year from the coverage ending date. Forms without coverage date - year from the receipt date.
- `spender_committee_designation` (array<string>, one of: A, J, P, U, B, D): The one-letter designation code of the organization: - A authorized by a candidate - J joint fundraising committee - P principal campaign c…
- `spender_committee_name` (array<string>): The name of the committee. If a committee changes its name, the most recent name will be shown. Committee names are not unique. Use committ…
- `spender_committee_type` (array<string>): The one-letter type code of the organization: - C communication cost - D delegate - E electioneering communication - H House - I independen…

### GET /schedules/schedule_h4/efile/
Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints.

**Query parameters:**
- `committee_id` (array<string>): A unique identifier assigned to each committee or filer registered with the FEC. In general a committee id begins with the letter C which i…
- `image_number` (array<string>): An unique identifier for each page where the electronic or paper filing is reported.
- `last_disbursement_amount` (number): When sorting by `disbursement_amount`, this is populated with the `disbursement_amount` of the last result. However, you will need to pass…
- `last_disbursement_purpose` (array<string>): When sorting by `disbursement_purpose`, this is populated with the `disbursement_purpose`of the last result. However, you will need to pass…
- `last_event_purpose_date` (string): When sorting by `event_purpose_date`, this is populated with the `event_purpose_date` of the last result. However, you will need to pass th…
- `max_amount` (number): Filter for all amounts less than a value.
- `max_date` (string): Maximum event_purpose_date
- `max_image_number` (string): Maxium image number of the page where the schedule item is reported
- `min_amount` (number): Filter for all amounts greater than a value.
- `min_date` (string): Minimum event_purpose_date
- `min_image_number` (string): Minium image number of the page where the schedule item is reported
- `payee_city` (array<string>): City of the entity that received the payment
- `payee_state` (array<string>): State of the entity that received the payment
- `payee_zip` (array<string>): Zip of the entity that received the payment
