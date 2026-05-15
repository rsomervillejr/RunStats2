# Data Model

## RunEntry

Represents a recorded running activity.

### Fields

- `id` (Integer, PK)
- `date` (Date, required)
- `total_distance_miles` (Numeric(6,3), required)
- `run_type` (String, required)
  - Allowed values: `race`, `workout`
- `environment` (String, required)
  - Allowed values: `treadmill`, `outdoor`
- `race_name` (String, nullable)
- `race_distance_miles` (Numeric(5,1), nullable)
- `notes` (Text, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Validation Rules

- `date` must be present and a valid date.
- `total_distance_miles` must be present and greater than zero.
- `run_type` must be one of the allowed values.
- `environment` must be one of the allowed values.
- `race_name`, `race_distance_miles`, and `notes` may be absent or null.
- If `race_distance_miles` is provided, it must be positive.
- `splits` must be a non-empty list of associated `MileSplit` values.

## MileSplit

Represents a single mile split for a run.

### Fields

- `id` (Integer, PK)
- `run_id` (Integer, FK to `RunEntry.id`, required)
- `split_index` (Integer, required)
- `distance_miles` (Numeric(5,3), required)
- `time_seconds` (Integer, required)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Constraints

- Unique constraint on `(run_id, split_index)` to preserve split ordering.
- `distance_miles` must be greater than zero.
- `time_seconds` must be greater than zero.

## Relationships

- `RunEntry` has many `MileSplit` records.
- Each `MileSplit` belongs to one `RunEntry`.

## State Transitions

- A run record can be created or updated while optional fields remain null.
- Update operations replace existing splits atomically and preserve nullable run metadata.
