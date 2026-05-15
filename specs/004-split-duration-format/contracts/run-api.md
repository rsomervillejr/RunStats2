# Run API Contract for Split Duration Format

## POST /api/runs

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

Split object fields:
- `split_index` (required): integer
- `distance_miles` (required): decimal
- `duration_mmss` (required): string in strict `mm:ss` format where minutes and seconds are each 00–59

Validation rules:
- `duration_mmss` is required for each split.
- `time_seconds` must not be included in split request objects.
- `duration_mmss` must match the pattern `^[0-5][0-9]:[0-5][0-9]$`.
- Converted split duration must be greater than 00:00.
- Split distances must sum to `total_distance_miles` within a small tolerance.

Response:
- `201 Created` with the created run object
- `400 Bad Request` for validation errors

## PUT /api/runs/{id}

Update an existing run. Request body is the same as POST.

Response:
- `200 OK` with updated run object
- `400 Bad Request` for validation errors
- `404 Not Found` if the run does not exist

## Error contract

The API returns validation failures as:
- `error`: string
- `details`: object with field-specific error messages

Example invalid payload error for prohibited `time_seconds` usage:
- `details`: {
    `splits`: [
      "API requests must not include time_seconds; use duration_mmss instead."
    ]
  }
