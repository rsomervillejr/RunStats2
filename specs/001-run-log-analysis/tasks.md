# Tasks: Run Log Analysis

**Input**: Design documents from `/specs/001-run-log-analysis/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD is mandatory per constitution - tests must be written and must fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Dependencies Graph

```
US1 (Create) → US2 (View) → US3 (Edit)
```

**MVP Scope**: User Story 1 (Create) + User Story 2 (View) provides basic run logging functionality.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create src/ directory structure per implementation plan
- [x] T002 Create tests/ directory structure per implementation plan
- [ ] T003 Initialize Python virtual environment and install Flask dependencies
- [x] T004 Configure PostgreSQL database connection and environment variables
- [ ] T005 Initialize Flask-Migrate for database schema management

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Flask application factory in src/app.py
- [x] T007 Configure SQLAlchemy database models base class in src/models/__init__.py
- [x] T008 Setup Marshmallow validation schemas base in src/api/schemas.py
- [x] T009 Create API blueprint structure in src/api/__init__.py
- [x] T010 Configure Flask-Migrate database migrations in src/migrations/
- [x] T011 Setup error handling and logging infrastructure in src/app.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a new run entry (Priority: P1) 🎯 MVP

**Goal**: Allow users to record a fresh workout or race by entering date, distance, type, environment, and mile split details

**Independent Test**: Enter a new run with at least one mile split, save it, and verify it appears in the history list

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Contract test for POST /api/runs endpoint in tests/contract/test_runs_api.py
- [x] T013 [P] [US1] Unit test for RunEntry model validation in tests/unit/test_models.py
- [x] T014 [P] [US1] Unit test for MileSplit model validation in tests/unit/test_models.py
- [x] T015 [P] [US1] Unit test for run creation service in tests/unit/test_services.py
- [x] T016 [US1] Integration test for creating run with splits in tests/integration/test_run_creation.py

### Implementation for User Story 1

- [x] T017 [P] [US1] Create RunEntry SQLAlchemy model in src/models/run_entry.py
- [x] T018 [P] [US1] Create MileSplit SQLAlchemy model in src/models/mile_split.py
- [x] T019 [P] [US1] Create Marshmallow schemas for run creation in src/api/schemas.py
- [x] T020 [US1] Implement run creation service in src/services/run_service.py
- [x] T021 [US1] Implement POST /api/runs endpoint in src/api/runs.py
- [x] T022 [US1] Add validation for race metadata when run_type is race
- [x] T023 [US1] Add validation for split distance sum matching total distance

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View run history and details (Priority: P1) 🎯 MVP

**Goal**: Allow users to browse previously entered runs, see them ordered by date, and inspect a selected entry at the mile split level

**Independent Test**: Open view mode, confirm the history list is sorted by date, select an entry, and verify the split details and chart display

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T024 [P] [US2] Contract test for GET /api/runs endpoint in tests/contract/test_runs_api.py
- [x] T025 [P] [US2] Contract test for GET /api/runs/{id} endpoint in tests/contract/test_runs_api.py
- [x] T026 [P] [US2] Unit test for run listing service in tests/unit/test_services.py
- [x] T027 [P] [US2] Unit test for run detail service in tests/unit/test_services.py
- [x] T028 [US1] Integration test for viewing run history and details in tests/integration/test_run_viewing.py

### Implementation for User Story 2

- [x] T029 [US2] Implement run listing service in src/services/run_service.py
- [x] T030 [US2] Implement run detail service in src/services/run_service.py
- [x] T031 [US2] Implement GET /api/runs endpoint in src/api/runs.py
- [x] T032 [US2] Implement GET /api/runs/{id} endpoint in src/api/runs.py
- [x] T033 [US2] Add pace calculation for splits in service layer
- [x] T034 [US2] Add date ordering (newest first) to run listing

**Checkpoint**: At this point, User Stories 1 & 2 should provide complete basic run logging functionality

---

## Phase 5: User Story 3 - Edit an existing run (Priority: P2)

**Goal**: Allow users to correct mistakes in previous entries by updating date, distance, type, environment, or split data

**Independent Test**: Select an existing run, switch to edit mode, change a field or split value, save, and confirm the updated entry appears in history

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T035 [P] [US3] Contract test for PUT /api/runs/{id} endpoint in tests/contract/test_runs_api.py
- [x] T036 [P] [US3] Unit test for run update service in tests/unit/test_services.py
- [x] T037 [US3] Integration test for editing existing runs in tests/integration/test_run_editing.py

### Implementation for User Story 3

- [x] T038 [US3] Implement run update service in src/services/run_service.py
- [x] T039 [US3] Implement PUT /api/runs/{id} endpoint in src/api/runs.py
- [x] T040 [US3] Add validation for update payloads matching creation rules
- [x] T041 [US3] Handle split replacement during updates

**Checkpoint**: At this point, all core CRUD functionality should be complete

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Frontend interface, error handling, and production readiness

- [x] T042 Create base HTML template in src/templates/base.html
- [x] T043 Create view mode template with run history list in src/templates/view.html
- [x] T044 Create edit mode template with run entry form in src/templates/edit.html
- [x] T045 Create run detail template with split chart in src/templates/detail.html (integrated into view.html)
- [ ] T046 Add Chart.js library to src/static/js/chart.js (using CDN)
- [x] T047 Implement JavaScript for dynamic split form fields in src/static/js/splits.js (integrated into edit.html)
- [x] T048 Implement JavaScript for Chart.js pace visualization in src/static/js/chart.js (integrated into view.html)
- [x] T049 Add frontend routes for view/edit mode switching in src/app.py
- [ ] T050 Add error page templates for 404 and 500 errors
- [ ] T051 Add form validation feedback in frontend JavaScript (basic validation implemented)
- [ ] T052 Configure production logging and error handling
- [ ] T053 Add database indexes for performance optimization
- [x] T054 Create comprehensive README.md with setup and usage instructions

---

## Implementation Strategy

**MVP First**: Complete Phase 1-4 (US1 + US2) for basic run logging functionality.

**Incremental Delivery**: Each user story can be developed and tested independently.

**Parallel Opportunities**: Marked with [P] - can be implemented simultaneously.

**Testing Strategy**: Contract tests first, then unit tests, then integration tests per user story.

**Success Criteria**:
- All tests pass (unit, integration, contract)
- Manual validation meets 90% success rate for core scenarios
- API follows REST principles and contract specifications
- Frontend provides intuitive view/edit modes with charting