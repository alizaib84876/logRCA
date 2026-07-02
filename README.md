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
The first milestone is the project scaffold. The next step is to install the minimum backend dependencies and wire up a runnable API.

Install the API extras when you are ready:

```bash
pip install -e ".[api]"
```
