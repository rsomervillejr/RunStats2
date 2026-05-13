# API Contract: RunStats2 Run Log

## Base URL

`/api`

## Endpoints

### GET /api/runs

Retrieve the historical run list ordered by date descending.

Response 200:
```json
[
  {
    "id": 1,
    "date": "2026-05-07",
    "total_distance_miles": 6.2,
    "run_type": "race",
    "environment": "outdoor",
    "race_name": "City 10K",
    "race_distance_miles": 6.2,
    "summary_pace_seconds_per_mile": 360,
    "split_count": 4
  }
]
```

### GET /api/runs/{run_id}

Retrieve a specific run with all mile split detail.

Response 200:
```json
{
  "id": 1,
  "date": "2026-05-07",
  "total_distance_miles": 6.2,
  "run_type": "race",
  "environment": "outdoor",
  "race_name": "City 10K",
  "race_distance_miles": 6.2,
  "notes": "Strong finish",
  "splits": [
    {
      "split_index": 1,
      "distance_miles": 1.0,
      "time_seconds": 360,
      "pace_seconds_per_mile": 360
    },
    {
      "split_index": 2,
      "distance_miles": 1.0,
      "time_seconds": 365,
      "pace_seconds_per_mile": 365
    },
    {
      "split_index": 3,
      "distance_miles": 1.0,
      "time_seconds": 355,
      "pace_seconds_per_mile": 355
    },
    {
      "split_index": 4,
      "distance_miles": 3.2,
      "time_seconds": 1140,
      "pace_seconds_per_mile": 356.25
    }
  ]
}
```

### POST /api/runs

Create a new run entry with nested split data.

Request 201:
- Creates one run and its associated splits.
- Returns the created run representation.

Request body:
```json
{
  "date": "2026-05-07",
  "total_distance_miles": 6.2,
  "run_type": "race",
  "environment": "outdoor",
  "race_name": "City 10K",
  "race_distance_miles": 6.2,
  "notes": "Strong finish",
  "splits": [
    {"split_index": 1, "distance_miles": 1.0, "time_seconds": 360},
    {"split_index": 2, "distance_miles": 1.0, "time_seconds": 365},
    {"split_index": 3, "distance_miles": 1.0, "time_seconds": 355},
    {"split_index": 4, "distance_miles": 3.2, "time_seconds": 1140}
  ]
}
```

Validation rules:
- `date`, `total_distance_miles`, `run_type`, and `environment` are required.
- `race_name` and `race_distance_miles` are required when `run_type` is `race`.
- `splits` must be a non-empty array.
- Sum of `splits[].distance_miles` must match `total_distance_miles` within tolerance.
- `split_index` values must be unique and sequential for display ordering.

### PUT /api/runs/{run_id}

Update an existing run entry and its nested split data.

Request body is the same as POST /api/runs.

Response 200:
- Returns the updated run object.

Validation rules are identical to create.

### DELETE /api/runs/{run_id}

Delete a run and its associated splits.

Response 204: No content.

## Error handling

- `400 Bad Request` for validation failures.
- `404 Not Found` when a requested run does not exist.
- `409 Conflict` for split ordering or data integrity violations.
- `500 Internal Server Error` for unexpected failures.

## Notes

- The API is designed to support a frontend charting layer by returning `pace_seconds_per_mile` for each split.
- The primary resource is `/api/runs`; split data is nested inside the run payload for create and update flows.
- The API is consumed by the Flask template-based frontend for data entry and visualization.
