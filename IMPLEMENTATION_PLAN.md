# LogRCA Implementation Plan

## Goal
Build an agentic RAG system for log-based incident root-cause analysis that can:
- answer natural-language incident questions
- search noisy operational logs and historical postmortems
- cite source evidence in answers
- self-correct when retrieval quality is weak
- evaluate retrieval and answer quality quantitatively
- expose the whole workflow in a web dashboard

## Guiding Constraints
- Start small and validate each layer before adding the next one.
- Install dependencies only when a phase needs them.
- Prefer a local, Apple Silicon-friendly development path first.
- Keep every milestone reproducible and documented in the progress file.
- Make regular Git commits after useful milestones and keep the work tree clean.
- Add CI/CD only when the project reaches the point where automated checks and deployment are meaningful.
- Use a GitHub repository as the long-term source of truth once the initial scaffold is stable.

## Recommended Build Strategy
Build the system in 8 phases:
1. project scaffold and environment
2. data ingestion and normalization
3. indexing and retrieval
4. orchestration and answer generation
5. citation verification
6. evaluation pipeline
7. API and dashboard
8. end-to-end validation and demo hardening

---

## Phase 0: Project Decisions
### Deliverables
- Finalize the tech stack choices that are easiest to run on a MacBook Air M4.
- Define the first demo scope.
- Define the initial dataset plan.

### Decisions to lock
- Backend: FastAPI
- Orchestration: LangGraph
- Vector store: Qdrant local container or local in-process fallback for early development
- Sparse retrieval: BM25 via rank_bm25 for the first local build, then optionally OpenSearch/Elasticsearch later
- Embeddings: bge-large-en-v1.5 or a smaller local substitute if memory becomes an issue
- Reranker: bge-reranker-large or a smaller reranker if local inference is too heavy
- Frontend: Streamlit for the first version, Chainlit only if conversational UX becomes important
- Evaluation: Ragas
- Log parsing: Drain3

### Exit criteria
- The stack is documented and frozen for the first implementation pass.
- The first demo dataset is chosen.

---

## Phase 1: Workspace Scaffold
### Deliverables
- Create the Python project structure.
- Create a virtual environment.
- Add config files for development, formatting, and reproducibility.
- Add a clear folder layout.

### Suggested folders
- `src/logrca/` core application code
- `src/logrca/ingestion/`
- `src/logrca/retrieval/`
- `src/logrca/orchestration/`
- `src/logrca/generation/`
- `src/logrca/evaluation/`
- `src/logrca/api/`
- `src/logrca/ui/`
- `data/raw/`
- `data/processed/`
- `data/indexes/`
- `tests/`
- `docs/`

### Install only when needed
- `python-dotenv`
- `pydantic`
- `fastapi`
- `uvicorn`
- `streamlit`
- `langgraph`

### Exit criteria
- The project runs locally with a minimal hello-world backend.
- The repository has a documented run path.

---

## Phase 2: Dataset and Ingestion
### Deliverables
- Load raw logs from a public dataset such as LogHub.
- Create a small synthetic postmortem dataset if real postmortems are not immediately available.
- Parse logs into structured records.
- Mine templates with Drain3.
- Normalize dynamic fields such as timestamps, IDs, IPs, hashes, and numeric noise.

### Tasks
- Define a unified schema for logs and postmortems.
- Implement ingestion adapters for raw text files and JSON or CSV sources.
- Store both raw and normalized versions.
- Chunk postmortems hierarchically so sections remain retrievable with context.

### Install only when needed
- `drain3`
- `pandas`
- `pyarrow` if columnar storage becomes useful

### Exit criteria
- A sample log file becomes structured templates plus metadata.
- Postmortem documents are chunked into retrievable units.

---

## Phase 3: Indexing Layer
### Deliverables
- Build dense embeddings for log templates and postmortem chunks.
- Build BM25 indices for exact keyword retrieval.
- Store metadata needed for time-window and service filtering.

### Tasks
- Choose chunk identifiers and metadata fields.
- Define index update flow.
- Persist vectors and sparse documents separately.
- Add an interface for filtering by service, time window, severity, and incident ID.

### Install only when needed
- `qdrant-client`
- `sentence-transformers`
- `rank_bm25`
- `numpy`
- Optional local serving backends if model loading requires them

### Exit criteria
- A query can retrieve top-k candidates from dense and sparse indices independently.
- Metadata filters are applied before ranking.

---

## Phase 4: Hybrid Retrieval
### Deliverables
- Merge dense and sparse results with Reciprocal Rank Fusion.
- Add reranking with a cross-encoder.
- Return evidence candidates with scores and source metadata.

### Tasks
- Implement retrieval APIs for dense, sparse, and fused search.
- Add service/time-window filters to all retrieval paths.
- Add reranker scoring on the fused shortlist.
- Preserve traceability back to original evidence.

### Install only when needed
- `sentence-transformers` if not already installed
- reranker model assets

### Exit criteria
- Retrieval returns a ranked evidence set with source references.
- The system can explain why an item was selected.

---

## Phase 5: Agentic Orchestration
### Deliverables
- Build a LangGraph workflow for question analysis, retrieval, grading, rewrite, and answer generation.
- Add a bounded self-correction loop.

### Tasks
- Classify the user query type.
- Estimate whether evidence is sufficient.
- If evidence is weak, widen the scope or rewrite the query.
- Cap retries to avoid loops.
- Emit a final structured result containing answer, evidence, confidence, and provenance.

### Install only when needed
- `langgraph`
- `langchain` or minimal LLM interface adapters if used in implementation

### Exit criteria
- Weak retrieval triggers a retry path rather than a hallucinated answer.
- Strong retrieval flows directly to answer generation.

---

## Phase 6: Citation-Constrained Generation
### Deliverables
- Generate answers only from retrieved evidence.
- Attach citations to log lines or postmortem sections.
- Verify that every citation exists in the retrieved context.

### Tasks
- Define a citation schema.
- Create a prompt template that requires evidence-backed claims.
- Add a citation validation step that rejects unsupported references.
- Surface confidence and citation status in the response.

### Exit criteria
- Answers are source-linked and citation-checked.
- Unsupported statements are flagged or removed.

---

## Phase 7: Evaluation Pipeline
### Deliverables
- Automated evaluation for retrieval and answer quality.
- Baseline metrics and repeatable evaluation runs.

### Metrics
- Context precision
- Context recall
- Faithfulness
- Answer relevance

### Tasks
- Build a small labeled evaluation set.
- Run Ragas on retrieval and generation outputs.
- Save scores per experiment run.
- Compare baseline keyword search versus hybrid retrieval.

### Install only when needed
- `ragas`
- `datasets`
- any evaluation-time model dependencies

### Exit criteria
- The project can produce measurable quality reports.
- Baseline numbers are reproducible.

---

## Phase 8: API and Dashboard
### Deliverables
- FastAPI endpoints for query, retrieval inspection, and evaluation results.
- Streamlit dashboard for querying and evidence inspection.
- Visualization of confidence and metrics.

### Tasks
- Add `/query`, `/health`, `/evidence`, and `/evaluation` endpoints.
- Build a dashboard panel for answer, evidence, citations, and metrics.
- Make the UI show the retrieval path and self-correction path when applicable.

### Exit criteria
- A user can submit a question and inspect evidence in one screen.
- The service runs end-to-end locally.

---

## Phase 9: Packaging and Demo Hardening
### Deliverables
- Docker support if needed.
- Reproducible start instructions.
- Demo dataset and demo script.
- Known limitations documented.
- GitHub repository setup if not already initialized.
- CI workflow for linting, tests, and basic validation.

### Tasks
- Add environment files and container configs only after local development is stable.
- Create a sample incident walkthrough.
- Record performance and limitations.

### Exit criteria
- Another person can clone, install, and run the project with the docs alone.

---

## Recommended Dependency Install Order
1. Python virtual environment and core packaging tools
2. Base app dependencies: FastAPI, Pydantic, dotenv, Uvicorn
3. Data tooling: pandas, pyarrow, Drain3
4. Retrieval tooling: rank_bm25, sentence-transformers, qdrant-client
5. Orchestration: langgraph
6. Evaluation: ragas and supporting packages
7. UI: streamlit
8. Optional infrastructure: Docker, OpenSearch, Elasticsearch

## Apple Silicon Notes
- Prefer lightweight local defaults first.
- Avoid assuming large models fit comfortably in memory.
- Start with smaller embedding and reranking models if the recommended ones are too heavy.
- Keep a CPU-first path working before optimizing for acceleration.

## Definition of Done
- Logs and postmortems are ingested and normalized.
- Hybrid retrieval works with filters and reranking.
- The agentic loop retries on weak evidence.
- Answers are cited and citation-checked.
- Evaluation scores are reproducible.
- A dashboard exposes the full flow.

## Build Principle
Do not install everything at once. Install only the dependencies required to complete the next unfinished phase, then validate that phase before moving on.

## Git and Delivery Policy
- Create a commit whenever a milestone produces a stable, meaningful improvement.
- Use concise commit messages that describe the delivered slice.
- Add CI/CD checks after the repo has a runnable baseline and a small test suite.
- If the project is not yet initialized as a Git repository, do that before the first milestone commit.
