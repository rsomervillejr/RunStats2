# Tasks: Split duration time format (mm:ss)

- [ ] T001 Confirm `specs/004-split-duration-format/spec.md` and `plan.md` accurately reflect the strict `mm:ss` requirement and `time_seconds` persistence.
- [ ] T002 Create `specs/004-split-duration-format/tasks.md` for implementation tracking.
- [ ] T003 Confirm no `quickstart.md` doc reference exists outside the feature docs and that API contract docs are up to date.

- [X] T004 [US1] Update request validation to accept and validate strict `mm:ss` split duration input.
- [X] T005 [US1] Add conversion logic from validated `mm:ss` into `MileSplit.time_seconds`.
- [X] T006 [US1] Modify `src/api/runs.py` request handling to reject invalid duration formats with HTTP 400.
- [X] T007 [US1] Ensure `run_service.py` persists split durations using existing `time_seconds` and rejects invalid values before saving.

- [X] T008 [P] [US2] Add unit tests for `mm:ss` validation and conversion in the split validation layer.
- [X] T009 [P] [US2] Add integration tests for valid and invalid split duration behavior on run creation.
- [X] T010 [P] [US2] Add integration tests for valid and invalid split duration behavior on run updates.
- [X] T011 [P] [US2] Add contract tests verifying invalid `mm:ss` input returns HTTP 400.

- [X] T012 [US3] Update `specs/004-split-duration-format/spec.md` and contracts/ notes to document strict `mm:ss` validation and `time_seconds` persistence.
- [X] T013 [US3] Run the full targeted test suite for this feature and confirm no regressions.
