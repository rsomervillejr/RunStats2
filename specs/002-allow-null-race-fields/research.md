# Research: Nullable race metadata and notes

## Decision

Allow `race_name`, `race_distance_miles`, and `notes` to be optional and nullable for run creation and updates.

## Rationale

- The existing domain model already treats race metadata as optional for non-race workouts.
- Requiring race data for all runs reduces usability and creates a poor experience for regular training entries.
- Keeping optional fields nullable preserves compatibility with existing records and avoids forcing clients to supply placeholder values.

## Implementation Approach

- Keep `race_name`, `race_distance_miles`, and `notes` as nullable columns in the `run_entries` table.
- Adjust Marshmallow schema validation so optional fields can be omitted or explicitly null.
- Preserve strict validation on required fields: `date`, `total_distance_miles`, `run_type`, `environment`, and `splits`.
- Continue validating provided race values if present, including positive numeric distance and non-empty race name when supplied.

## Alternatives Considered

1. Enforce race metadata only for `run_type == race`.
   - Rejected because the feature explicitly requires `race` records to allow null race fields.

2. Introduce a separate race metadata object or nested endpoint.
   - Rejected because it would be overkill for a small optional-field change and would require larger API/DB changes.

3. Treat empty strings as equivalent to null.
   - Not chosen as the primary design; instead, the system should accept explicit null and allow clients to send absent fields.

## Outcome

The chosen design minimizes disruption, uses existing nullable DB columns, and keeps the API contract stable while improving flexibility for users.
