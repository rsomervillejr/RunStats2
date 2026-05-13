# Data Model: Run Log Analysis

## Entities

### RunEntry

- `id`: integer, primary key
- `date`: date, required
- `total_distance_miles`: numeric(6,3), required, > 0
- `run_type`: enum(`race`, `workout`), required
- `environment`: enum(`treadmill`, `outdoor`), required
- `race_name`: string, required when `run_type == race`
- `race_distance_miles`: numeric(5,1), required when `run_type == race`
- `notes`: text, optional
- `created_at`: timestamp, auto-set
- `updated_at`: timestamp, auto-updated

### MileSplit

- `id`: integer, primary key
- `run_id`: foreign key to `RunEntry.id`, required
- `split_index`: integer, required, 1-based order
- `distance_miles`: numeric(5,3), required, > 0
- `time_seconds`: integer, required, > 0
- `pace_seconds_per_mile`: numeric(7,3), computed or optionally stored for convenience
- `created_at`: timestamp, auto-set
- `updated_at`: timestamp, auto-updated

## Relationships

- `RunEntry` 1-to-many `MileSplit`
- Each `MileSplit` belongs to exactly one `RunEntry`
- `MileSplit.split_index` must be unique per `RunEntry`

## Validation rules

- `RunEntry.date` must be present and a valid date.
- `RunEntry.total_distance_miles` must be greater than 0.
- `RunEntry.run_type` must be either `race` or `workout`.
- `RunEntry.environment` must be either `treadmill` or `outdoor`.
- When `run_type == race`, `race_name` and `race_distance_miles` are mandatory.
- A run must contain at least one `MileSplit`.
- The sum of `MileSplit.distance_miles` values for a run must equal `RunEntry.total_distance_miles` within a small tolerance (e.g., 0.001 miles).
- Each split must have `time_seconds > 0` and `distance_miles > 0`.
- The final split distance may be fractional to support non-whole-mile totals.

## Query patterns

- List runs ordered by `date DESC` for history view.
- Retrieve a run and its splits in a single joined query for detail and charting.
- Validate and persist nested split payloads atomically to ensure run integrity.

## Implementation notes

- Use SQLAlchemy `Numeric` for mile distances to preserve decimal precision.
- Store raw split time in seconds and compute pace values as `time_seconds / distance_miles`.
- Keep split ordering explicit through `split_index` to support sequential display and chart x-axis ordering.
- Provide `pace_seconds_per_mile` in API responses so frontend charting can use a simple numeric series.
