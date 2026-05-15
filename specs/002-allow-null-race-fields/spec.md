# Feature Specification: Allow nullable race metadata and notes

**Feature Branch**: `002-allow-null-race-fields`  
**Created**: May 13, 2026  
**Status**: Draft  
**Input**: User description: "Allow null entires for fields: \"race_name\", \"race_distance_miles\" and \"notes\"."

## Clarifications

### Session 2026-05-14
- Q: How should empty string `race_name` values be handled? → A: Convert empty string to null so race metadata is normalized.
- Q: When zero is entered for `race_distance_miles`, how should it be handled? → A: Convert zero to null so race metadata is normalized.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Optional race metadata on run entry (Priority: P1)

A runner wants to record a run without forcing optional race details when they are unknown or not relevant.

**Why this priority**: This improves usability by removing unnecessary required fields for runs that do not have full race metadata.

**Independent Test**: Submit a run creation request with `race_name`, `race_distance_miles`, and `notes` missing or null and verify the run is created successfully.

**Acceptance Scenarios**:

1. **Given** a user creates a workout run, **when** they omit `race_name` and `race_distance_miles`, **then** the run is accepted and stored successfully.
2. **Given** a user creates a race run, **when** they provide `run_type` = `race` but leave `race_name` and `race_distance_miles` null, **then** the run is accepted and stored with null race metadata.
3. **Given** a user submits a run without `notes`, **when** the request is processed, **then** the run is stored and the `notes` field remains null.
4. **Given** a user submits `race_name` as an empty string, **when** the request is processed, **then** the system stores `race_name` as null.
5. **Given** a user submits `race_distance_miles` as zero, **when** the request is processed, **then** the system stores `race_distance_miles` as null.

---

### User Story 2 - Update existing runs without requiring notes or race fields (Priority: P2)

A runner wants to edit an existing run record without having to re-enter optional fields that were not initially provided.

**Why this priority**: This preserves existing run editing workflows and makes updates less error-prone.

**Independent Test**: Update a run record while omitting or nulling `race_name`, `race_distance_miles`, and `notes` and confirm the update succeeds.

**Acceptance Scenarios**:

1. **Given** an existing run without notes, **when** the user updates another field, **then** the run remains valid and the `notes` field stays null.
2. **Given** an existing race run with empty race metadata, **when** the user updates the run, **then** the system allows the record to persist with null race metadata.

---

### User Story 3 - API and schema support for nullable race and notes fields (Priority: P3)

Developers and API consumers need the system to accept and return null values for optional run fields consistently.

**Why this priority**: Ensures API contract clarity and avoids breaking existing clients by changing field requirements.

**Independent Test**: Verify API schema validation accepts null values for `race_name`, `race_distance_miles`, and `notes`, and that responses include null for unset optional fields.

**Acceptance Scenarios**:

1. **Given** an API client submits a run payload with null optional fields, **when** the schema validates data, **then** validation passes.
2. **Given** the system returns run details for a record with no race metadata, **when** the API response is generated, **then** `race_name`, `race_distance_miles`, and `notes` are present as null values or omitted consistently.

---

### Edge Cases

- Empty string `race_name` values MUST be normalized to null, consistent with explicit null handling.
- Zero `race_distance_miles` values MUST be normalized to null, consistent with explicit null handling.
- How should clients distinguish between "field omitted" and "field intentionally null"?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow `race_name` to be null for all run creation and update requests.
- **FR-002**: System MUST allow `race_distance_miles` to be null for all run creation and update requests.
- **FR-003**: System MUST allow `notes` to be null or absent for all run creation and update requests.
- **FR-004**: System MUST continue to validate required run fields such as date, total distance, run type, environment, and split data.
- **FR-005**: If optional race metadata is provided, system MUST validate it according to existing race rules (for example, distance must be positive when present).
- **FR-006**: System MUST preserve null values for `race_name`, `race_distance_miles`, and `notes` in stored records and API responses.
- **FR-007**: System MUST allow existing run update workflows to succeed without requiring optional values.
- **FR-008**: System MUST normalize any empty string provided for `race_name` to null before persisting or returning run data.
- **FR-009**: System MUST normalize a provided value of zero for `race_distance_miles` to null before persisting or returning run data.

### Key Entities *(include if feature involves data)*

- **RunEntry**: Run record including date, total distance, type, environment, optional race metadata, and optional notes.
- **MileSplit**: Associated split records for each mile segment, unchanged by this feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid run creation requests that omit `race_name`, `race_distance_miles`, or `notes` are accepted.
- **SC-002**: 100% of valid run update requests that omit or null these fields succeed without validation errors.
- **SC-003**: API responses for runs with missing optional metadata include null values or omit the fields consistently in at least 95% of cases.
- **SC-004**: No regression occurs for mandatory run validation rules; required fields still prevent invalid requests.

## Assumptions

- `race_name`, `race_distance_miles`, and `notes` are optional values used for richer metadata but are not required for core run logging.
- `run_type` remains the governing field for whether a run is a workout or race; race metadata may still be null.
- Existing database schema allows nullable values for these fields or can be updated to support them.
- Clients understand that null means "not provided" and should handle null fields gracefully.
