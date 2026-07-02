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
- CI workflow configured to run code-only tests on push and pull request
- Dataset-backed ingestion tests are tagged as integration tests for later runs

The next planned milestone is to use the ingestion outputs as the basis for retrieval indexes and quality checks.
