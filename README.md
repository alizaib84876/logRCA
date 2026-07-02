# LogRCA

Agentic retrieval-augmented generation for log-based incident root-cause analysis.

## Current state
- Project scaffold created.
- Implementation proceeds in phases so dependencies are installed only when needed.

## Planned stack
- Backend: FastAPI
- Orchestration: LangGraph
- Template mining: Drain3
- Sparse retrieval: BM25
- Vector search: Qdrant
- Reranking: bge-reranker-large or a smaller local fallback
- Evaluation: Ragas
- UI: Streamlit

## Local development
This repository currently contains the initial project scaffold and the first runnable FastAPI slice.

### Setup
Install the API extras when you want to run the backend locally:

```bash
pip install -e ".[api]"
```

### Current status
- Project scaffold completed
- Minimal FastAPI health endpoint available
- Ingestion status endpoint available for the HDFS_2k dataset
- HDFS_2k template mining and processed exports are wired into the ingestion pipeline
- First BM25 retrieval index over the processed HDFS_2k output is available locally
- BM25 retrieval is exposed through a backend search endpoint
- CI workflow configured to run code-only tests on push and pull request
- Dataset-backed ingestion tests are tagged as integration tests for later runs

The push workflow is intentionally kept dataset-free so it stays green on every commit. Dataset-backed checks stay in the integration test lane until a separate data-aware workflow is added.

The backend now also exposes a BM25 retrieval endpoint for local incident-style search over the processed HDFS_2k output.

The next planned milestone is to improve retrieval quality with ranking and hybrid search on top of the sparse index.
