# Tasks: Allow nullable race metadata and notes

**Input**: Design documents from `specs/002-allow-null-race-fields/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the feature branch, documentation, and artifacts for implementation.

- [ ] T001 Create and verify feature branch `002-allow-null-race-fields`
- [x] T002 Confirm `specs/002-allow-null-race-fields/spec.md` exists and reflects the nullable field requirement
- [x] T003 Create `specs/002-allow-null-race-fields/tasks.md` for implementation tracking
- [x] T004 Confirm `specs/002-allow-null-race-fields/plan.md`, `research.md`, `data-model.md`, and `contracts/run-api.md` are present and up to date

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Validate the current run model, schema, and service flow before applying nullable-field changes.

**⚠️ CRITICAL**: No story work should begin until this phase is complete.

- [x] T005 Review `src/models/run_entry.py` to confirm `race_name`, `race_distance_miles`, and `notes` are nullable columns
- [x] T006 Review `src/schemas.py` `RunEntrySchema` validation rules for optional race metadata and notes
- [x] T007 Review `src/services/run_service.py` create/update logic for handling optional run fields
- [x] T008 Review `src/api/runs.py` POST and PUT request handling for optional null fields
- [x] T009 Confirm whether a database migration is required for nullable race metadata and notes fields and add one if needed

**Checkpoint**: Foundational review complete and existing model/service behavior understood.

---

## Phase 3: User Story 1 - Optional race metadata on run entry (Priority: P1) 🎯 MVP

**Goal**: Allow run creation without requiring `race_name`, `race_distance_miles`, or `notes`.

**Independent Test**: Submit a POST /api/runs payload with no `race_name`, `race_distance_miles`, or `notes` and confirm the run is created successfully.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Add unit test for `RunService.create_run` accepting null/omitted `race_name`, `race_distance_miles`, and `notes` in `tests/unit/test_services.py`
- [x] T011 [P] [US1] Add integration test for POST `/api/runs` with missing optional fields in `tests/integration/test_run_creation.py`

### Implementation for User Story 1

- [x] T012 [US1] Update `src/schemas.py` `RunEntrySchema` to allow absent or null `race_name`, `race_distance_miles`, and `notes`
- [x] T013 [US1] Update `src/services/run_service.py` `create_run` to persist nullable optional fields
- [x] T014 [US1] Update `src/api/runs.py` POST `/api/runs` handling so the response preserves null optional fields
- [x] T015 [US1] Update `specs/002-allow-null-race-fields/contracts/run-api.md` to document nullable race metadata and notes

**Checkpoint**: Run creation supports optional nullable race metadata and notes.

---

## Phase 4: User Story 2 - Update existing runs without requiring optional fields (Priority: P2)

**Goal**: Allow run updates while leaving `race_name`, `race_distance_miles`, and `notes` null or omitted.

**Independent Test**: Submit a PUT /api/runs/{id} payload with missing or null optional fields and confirm the update succeeds.

### Tests for User Story 2 ⚠️

- [x] T016 [P] [US2] Add unit test for `RunService.update_run` accepting null/omitted optional fields in `tests/unit/test_services.py`
- [x] T017 [P] [US2] Add integration test for PUT `/api/runs/{id}` with nullable optional fields in `tests/integration/test_run_editing.py`

### Implementation for User Story 2

- [x] T018 [US2] Update `src/services/run_service.py` `update_run` to preserve null optional fields and handle absent values
- [x] T019 [US2] Update `src/api/runs.py` PUT `/api/runs/{id}` handling so the response preserves null optional fields
- [x] T020 [US2] Add regression coverage for editing a run without notes and verifying `notes` remains null

**Checkpoint**: Run editing supports nullable optional fields without requiring them.

---

## Phase 5: User Story 3 - API and schema support for nullable race and notes fields (Priority: P3)

**Goal**: Ensure API contract and response serialization consistently support null optional fields.

**Independent Test**: Verify API responses include `race_name`, `race_distance_miles`, and `notes` as null for records without those values.

### Tests for User Story 3 ⚠️

- [x] T021 [P] [US3] Add contract tests for nullable `race_name`, `race_distance_miles`, and `notes` in `tests/contract/test_runs_api.py`
- [x] T022 [P] [US3] Add integration test verifying GET `/api/runs/{id}` returns null optional fields in `tests/integration/test_run_creation.py`

### Implementation for User Story 3

- [x] T023 [US3] Update `src/services/run_service.py` `get_runs` and `get_run_by_id` serialization to return `None` for missing optional fields
- [x] T024 [US3] Update `src/schemas.py` response schemas if needed to explicitly allow null values for optional fields
- [x] T025 [US3] Add or update README/docs if the API contract behavior changes for nullable optional fields

**Checkpoint**: API contract and serialization handle nullable optional fields consistently.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Ensure documentation, tests, and feature notes are complete.

- [ ] T026 [P] [Story] Run full targeted test suite for this feature: `pytest tests/unit/test_services.py tests/integration/test_run_creation.py tests/integration/test_run_editing.py tests/contract/test_runs_api.py`
- [ ] T027 [P] [Story] Confirm `specs/002-allow-null-race-fields` documentation is consistent with implementation
- [ ] T028 [Story] Update `README.md` or feature notes if nullable API behavior needs to be surfaced to users
- [ ] T029 [Story] Clean up any temporary test fixtures or draft documentation in `specs/002-allow-null-race-fields/`

---

## Dependencies & Execution Order

- Phase 1 tasks are independent and can start immediately.
- Phase 2 tasks must complete before any user story implementation begins.
- User stories may proceed in priority order; stories can be worked on in parallel once foundational work is complete.
- Final polish tasks depend on the implementation and test tasks completing successfully.
