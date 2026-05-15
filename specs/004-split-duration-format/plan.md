# Implementation Plan for Split Duration Format

## Technical Context

This feature enforces a strict format for split durations in the application. The following decisions have been made:

- **Default Split Distance**: 1 mile (not adaptable to user unit preferences).
- **Split Duration Format**: Strictly `mm:ss`.
  - Minutes (`mm`) and seconds (`ss`) must each be in the range 0–59.
- **Validation**: The server will reject invalid formats with an HTTP 400 status code.

## Constitution Check

- **TDD Compliance**: Tests must be written before implementation.
- **Test Coverage**: Ensure ≥ 80% coverage.
- **Input Validation**: Use Marshmallow for validation.
- **RESTful API**: Ensure proper HTTP methods and status codes.
- **SQLAlchemy**: Use for database interactions.
- **JWT Authentication**: Maintain existing authentication mechanisms.

## Implementation Phases

### Phase 1: Schema and Validation Updates
- Update the request validation layer to accept a strict `mm:ss` duration input for split rows.
- Convert validated `mm:ss` values into the existing `time_seconds` field used by `MileSplit`.

Status: Completed — `MileSplitRequestSchema` now requires `duration_mmss` and converts to `time_seconds` on load.

### Phase 2: API Updates
- Modify the `runs.py` API to validate split durations during run creation and updates.
- Return HTTP 400 for invalid `mm:ss` formats or out-of-range minutes/seconds.

Status: Completed — `_validate_api_split_durations` enforces the request contract and rejects `time_seconds` in requests.

### Phase 3: Service Layer Updates
- Update `run_service.py` so that it persists `time_seconds` values derived from valid split durations.
- Ensure invalid duration input is rejected before database persistence.

Status: Completed — `RunService` uses schema-validated `time_seconds` when creating/updating `MileSplit` records.

### Phase 4: Testing
- Write unit tests for split duration validation and conversion logic.
- Write integration tests for `runs.py` API creation/update paths.
- Write contract tests to ensure the API rejects invalid formats and preserves `time_seconds` semantics.

Status: Completed — Added unit tests (`tests/unit/test_schemas.py`), contract tests, and integration tests covering creation and updates.

### Phase 5: Documentation
- Update the feature-level docs in `specs/004-split-duration-format` to include examples of valid and invalid split durations.
- Document the validation rules and the `time_seconds` persistence behavior in the API contract.

Status: In-progress — `spec.md` updated to require `duration_mmss` and document rejection of `time_seconds` in requests; recommend committing and opening PR.

Next Steps:
- Commit changes, run full test suite, open PR for review.
- Update any external API contract docs or consumer guides to reflect the `duration_mmss` request requirement.

## Dependencies

- Data model updates must precede API and service layer changes.
- Testing depends on the completion of data model and API updates.
- Documentation updates depend on the completion of all other phases.