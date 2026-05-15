# Run API Contract

## Endpoints

### GET /api/runs

List all runs ordered by date descending.

Response:
- `200 OK`
- JSON array of run summaries

Run summary object:
- `id`: integer
- `date`: date string
- `total_distance_miles`: decimal
- `run_type`: string
- `environment`: string
- `race_name`: string or null
- `race_distance_miles`: decimal or null
- `summary_pace_seconds_per_mile`: decimal
- `split_count`: integer

### GET /api/runs/{id}

Retrieve a single run with mile split details.

Response:
- `200 OK` with run object
- `404 Not Found` if run does not exist

Run object fields:
- `id`: integer
- `date`: date string
- `total_distance_miles`: decimal
- `run_type`: string
- `environment`: string
- `race_name`: string or null
- `race_distance_miles`: decimal or null
- `notes`: string or null
- `created_at`: timestamp
- `updated_at`: timestamp
- `splits`: array of split objects

Split object fields:
- `split_index`: integer
- `distance_miles`: decimal
- `time_seconds`: integer
- `pace_seconds_per_mile`: decimal

### POST /api/runs

Create a new run.

Request body:
- `date` (required): date string
- `total_distance_miles` (required): decimal
- `run_type` (required): `race` or `workout`
- `environment` (required): `treadmill` or `outdoor`
- `race_name` (optional): string, blank strings are normalized to null, or null
- `race_distance_miles` (optional): decimal, zero is normalized to null, or null
- `notes` (optional): string or null
- `splits` (required): non-empty array of split objects

Response:
- `201 Created` with created run object
- `400 Bad Request` for validation errors

### PUT /api/runs/{id}

Update an existing run.

Request body: same as POST.

Response:
- `200 OK` with updated run object
- `400 Bad Request` for validation errors
- `404 Not Found` if run does not exist

## Nullable Field Rules

- `race_name`, `race_distance_miles`, and `notes` may be omitted or explicitly null.
- Blank `race_name` values are normalized to null.
- `race_distance_miles` values of zero are normalized to null; non-zero values must be positive.
- The API preserves null values for these optional fields in responses.

## Validation Contracts

- `date`: required, valid date
- `total_distance_miles`: required, positive
- `run_type`: required, one of `race`, `workout`
- `environment`: required, one of `treadmill`, `outdoor`
- `splits`: required, length > 0
- `split.distance_miles`: required, positive
- `split.time_seconds`: required, positive
- Sum of all `splits.distance_miles` must equal `total_distance_miles` within a small tolerance
