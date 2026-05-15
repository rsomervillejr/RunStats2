# Feature Specification: Split duration time format (mm:ss)

**Feature Branch**: `004-split-duration-format`  
**Created**: May 15, 2026  
**Status**: Draft  
**Input**: User description: "The run entry screen should require the end user to enter mile split duration with minutes and seconds in the time format of \"mm:ss\". The minute and second values should be limited to a maximum of 59, with appropriate data entry validations to guide the user. The final mile split duration entered by the user can be converted into total seconds to retain consistency with the database structure."

## Clarifications

### Session 2026-05-15
Q1: Decision: The system will accept only strict `mm:ss` format for split duration input — alternate formats are not allowed.
Q2: Decision: The server MUST reject non-conforming formats and return HTTP 400 with a validation error; it will not attempt to coerce ambiguous inputs.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Require `mm:ss` split duration input (Priority: P1)

A runner entering split times must provide them in `mm:ss` format so the UI enforces consistent data entry and prevents ambiguous durations.

**Why this priority**: Ensures consistent UX and prevents downstream data issues caused by free-text duration entries.

**Independent Test**: Add a split row and enter `05:30`; save the run and verify the system persists `330` seconds for that split.

**Acceptance Scenarios**:

1. **Given** a user adds a split and enters `05:30`, **when** the run is saved, **then** the database stores `330` seconds for that split.
2. **Given** a user enters `5:3` or `5:03`, **when** the system validates input, **then** the input is rejected with HTTP 400 and a clear validation message (strict `mm:ss` required).
3. **Given** a user enters `60:00` or `00:60`, **when** validation runs, **then** input is rejected because minutes and seconds must be within 0–59.

---

### User Story 2 - Friendly inline validation and guidance (Priority: P2)

The UI guides users with inline hints and prevents invalid minutes/seconds (>59) at data entry time.

**Independent Test**: Try to enter `99:99` and verify the input control shows an inline error and prevents submission.

**Acceptance Scenarios**:

1. **Given** the user types `99:99` into the split duration field, **when** they move focus away, **then** an inline validation error appears and submission is blocked.
2. **Given** the user types non-numeric characters other than colon (e.g., `aa:bb`), **when** validation runs, **then** the input is rejected and guidance shown.

---

### User Story 3 - Conversion to total seconds for persistence (Priority: P3)

The server requires `duration_mmss` in requests and performs the conversion to integer seconds (`time_seconds`) for persistence. Requests that include `time_seconds` directly are rejected with HTTP 400 — the canonical request contract is `duration_mmss: "mm:ss"`.

**Why this priority**: Keeps storage consistent, simplifies computations (e.g., pace calculations), and avoids ambiguous client-submitted integer semantics.

**Independent Test**: Submit a run with `duration_mmss` values and verify the server stores the converted integer `time_seconds` values. Submitting `time_seconds` in the request should return HTTP 400.

**Acceptance Scenarios**:

1. **Given** the client submits `mm:ss`, **when** the server accepts and converts, **then** the stored value equals the converted seconds.
2. **Given** the client submits `time_seconds` in the request payload, **when** the server validates the payload, **then** the request is rejected with HTTP 400 and a clear validation message indicating `time_seconds` is not allowed in requests.

---

### Edge Cases

- Handling leading/trailing whitespace in input.
- Handling single-digit minutes or seconds (`5:3` should be interpreted as `05:03` if coercion allowed).
- Accessibility: screen readers should announce the expected `mm:ss` format.
- Timeouts or extremely long durations: reject minutes or seconds > 59.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The split duration input MUST enforce `mm:ss` time format on the run entry screen.
- **FR-002**: Minutes and seconds MUST each be in the range `0`–`59` inclusive.
- **FR-003**: The UI MUST show inline validation messages for malformed or out-of-range input and prevent submission until corrected.
- **FR-004**: The system MUST convert `mm:ss` into total seconds (integer) before persisting to the database; alternatively, the server MUST perform equivalent conversion if client does not.
 **FR-005**: The server-side API MUST validate the split duration format and converted seconds (must be positive and within reasonable bounds); on validation failure the API MUST return HTTP 400.
- **FR-006**: The API contract MUST document that split durations are stored as integer seconds and accepted input formats.

### Key Entities

- **SplitRow**: UI element containing `split_index`, `distance`, and `duration_mmss` (display value) plus `duration_seconds` (persisted value).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of split duration inputs entered in `mm:ss` are successfully converted to integer seconds on save.
- **SC-002**: Inline validation prevents >95% of malformed submissions in manual tests.
- **SC-003**: No accepted split duration value has minutes or seconds outside 0–59.

## Assumptions

- Client UI is capable of parsing and validating `mm:ss` inputs and displaying inline errors.
- Server persists split durations as integer seconds in the existing split model.
- The API accepts `mm:ss` formatted duration strings only; integer-second submissions are considered non-conforming and will be rejected.
