# LogRCA Progress Tracker

## How to use this file
- Update this file after every meaningful milestone.
- Keep notes short and factual.
- Record what was completed, what is blocked, what was learned, and what the next action is.
- If a future session resumes work, it should read this file first.

## Current Status
- Project has been defined at a high level.
- Initial project scaffold has been created.
- Implementation will now move into the first runnable backend milestone.
- Commit cadence should stay sparse and milestone-based.
- Dataset downloads will be requested only when the ingestion phase starts.
- Ingestion phase is now active with the first data model and loader scaffolding.

## Completed
- [x] Captured the project goal and core architecture in the implementation plan.
- [x] Established a phased delivery strategy that installs dependencies only when needed.
- [x] Defined a progress file for handoff continuity.
- [x] Created the initial Python project scaffold.
- [x] Verified the new Python files compile cleanly.
- [x] Installed the minimum API dependencies (`fastapi`, `uvicorn`).
- [x] Added GitHub/CI-CD delivery policy notes to the implementation plan.
- [x] Added a minimal CI workflow and smoke test.
- [x] Created the first Git commit for the scaffolded backend milestone.
- [x] Connected the local repository to GitHub and pushed `main`.
- [x] Moved the HDFS_2k dataset into the workspace and wired the first ingestion loader.
- [x] Validated the HDFS_2k ingestion test against the real dataset files.
- [x] Added Drain3-based template mining for HDFS_2k and validated it with tests.
- [x] Persisted mined HDFS_2k outputs into the processed data folder and validated the export pipeline.
- [x] Added an ingestion status helper and exposed it through the FastAPI backend.
- [x] Added API coverage for the HDFS_2k ingestion status endpoint.

## In Progress
- [ ] Wire up the first executable FastAPI entrypoint.
- [ ] Start the retrieval index layer using the processed HDFS_2k outputs.

## Validation Notes
- `pytest` initially failed because the src layout was not on `sys.path` during test collection.
- `python3 -m py_compile` passed for the new package files.
- API dependencies were installed successfully in the configured Python environment.
- `pytest` passed with the initial health-route smoke test.
- GitHub Actions failed because the workflow did not install the dev/test dependency set; the workflow now uses `.[api,dev]`.
- The new ingestion modules compile cleanly.
- The HDFS_2k loader test passed against the actual dataset in `data/raw/hdfs_2k/`.
- The Drain3-based template mining tests passed on the real HDFS_2k dataset.
- The ingestion export pipeline test passed and wrote processed CSV outputs into a temporary folder.
- The ingestion status endpoint test passed through the FastAPI app.

## Blockers
- None yet.

## Next Recommended Step
- Start the retrieval index layer using the processed HDFS_2k outputs.

## Suggested Milestone Sequence
1. Create the Python environment and project skeleton.
2. Add ingestion code for a tiny sample log dataset.
3. Implement template mining and normalization.
4. Add dense and sparse retrieval with filters.
5. Add RRF fusion and reranking.
6. Add LangGraph orchestration and retry logic.
7. Add cited answer generation and citation verification.
8. Add Ragas evaluation.
9. Build the FastAPI and Streamlit interface.
10. Package and document the final demo.

## Session Notes
- 2026-07-02: Started with an empty workspace; added the implementation plan and live progress tracker.
- 2026-07-02: Created the project scaffold and prepared the backend milestone.
- 2026-07-02: Installed the API dependencies and documented GitHub/CI-CD workflow expectations.
- 2026-07-02: Connected the GitHub remote and pushed the initial project state.
- 2026-07-02: Updated the plan to avoid excessive commits and to request datasets only during the relevant phase.
- 2026-07-02: Fixed the CI workflow so GitHub Actions installs both API and test dependencies.
- 2026-07-02: Added ingestion scaffolding and requested the LogHub HDFS dataset for phase 2.
- 2026-07-02: Moved the HDFS_2k dataset into the workspace and verified ingestion against the real files.
- 2026-07-02: Added Drain3 template mining for HDFS_2k and validated it against the dataset.
- 2026-07-02: Added persistence for the mined HDFS_2k output and verified the export pipeline.
- 2026-07-02: Added an ingestion status endpoint and verified it through the FastAPI app.
