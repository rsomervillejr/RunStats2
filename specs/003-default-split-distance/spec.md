# Feature Specification: Default mile split distance

**Feature Branch**: `003-default-split-distance`  
**Created**: May 15, 2026  
**Status**: Draft  
**Input**: User description: "The run entry screen should default the mile split distance to 1."

## Clarifications

### Session 2026-05-15
Q1: Decision: The run entry split distance default MUST be `1` mile for newly added split rows. The UI will not automatically convert this default to kilometers in v1.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Default split distance on new run entry (Priority: P1)

A runner opens the run entry screen and expects new split rows to pre-fill the distance with a sensible default so they can quickly log runs without typing repetitive values.

**Why this priority**: This reduces friction when logging runs and speeds up common workflows for users who typically run mile-based splits.

**Independent Test**: Open the run entry UI, add a new split row and verify the `distance_miles` input is pre-filled with `1`.

**Acceptance Scenarios**:

1. **Given** a user opens the run entry screen, **when** they add the first split row, **then** the split `distance` input is pre-filled with `1`.
2. **Given** a user adds additional split rows, **when** new rows are inserted, **then** each new row's `distance` input is pre-filled with `1`.

---

### User Story 2 - Users can override the default (Priority: P2)

A runner wants to change the default split distance for a specific run (e.g., 0.5 mile intervals).

**Why this priority**: Users must be able to provide accurate split distances; the default should not prevent specifying custom values.

**Independent Test**: Add a new split and change its distance to `0.5`; save the run and confirm the stored split uses `0.5`.

**Acceptance Scenarios**:

1. **Given** a new split is pre-filled with `1`, **when** the user edits that field to `0.5` and saves, **then** the persisted split distance is `0.5`.

---

### User Story 3 - Defaults adapt to unit preference (Priority: P3)

NOTE: Defaults will not adapt to user unit preference in v1. Support for adapting defaults to per-user units is deferred to a future enhancement.

---

### Edge Cases

- How should the UI behave if the user's unit preference is unknown? (assume miles by default)
- What happens when fractional defaults are desired (e.g., 0.25 miles)? The UI must accept decimal inputs.
- Accessibility: default values must be announced to assistive technologies and focus should land sensibly.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The run entry UI MUST pre-fill the split `distance` input with `1` for newly added split rows.
- **FR-002**: Users MUST be able to edit the pre-filled split `distance` before saving.
- **FR-003**: When a user edits a split distance, the system MUST persist the user-provided value.
 **FR-004**: The default behavior MUST pre-fill new split rows with `1` mile and NOT auto-convert to other units in v1.
- **FR-005**: The UI MUST accept decimal values and validate split distances as positive numbers.

### Key Entities *(include if feature involves data)*

- **RunEntryForm**: Client-side form for creating/editing runs; contains a list of `SplitRow` items.
- **SplitRow**: UI element representing a mile split; attributes include `split_index` and `distance`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of new split rows are pre-filled with `1` on the run entry screen within the target UI platforms (web/mobile).
- **SC-002**: At least 95% of users can create a run with default splits without manual typing for split distances in common scenarios (measured via usability testing or analytic events).
- **SC-003**: No regressions in split validation; invalid values are rejected with clear messages.

## Assumptions

- The application supports a single default distance value per new split row; advanced presets are out of scope for v1.
- The underlying data model already stores split distances as decimals and supports persisting arbitrary positive values.
- Regional unit preferences may exist; for this feature the default split distance is explicitly `1` mile.
