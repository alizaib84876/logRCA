from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="LogRCA", version="0.1.0")

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ingestion/hdfs-2k/status")
    def hdfs_2k_status() -> dict[str, int | str | bool]:
        from logrca.ingestion import build_hdfs_2k_ingestion_status

        status = build_hdfs_2k_ingestion_status()
        return {
            "dataset_name": status.dataset_name,
            "raw_log_exists": status.raw_log_exists,
            "structured_csv_exists": status.structured_csv_exists,
            "templates_csv_exists": status.templates_csv_exists,
            "mined_records_csv_exists": status.mined_records_csv_exists,
            "cluster_templates_csv_exists": status.cluster_templates_csv_exists,
            "raw_log_rows": status.raw_log_rows,
            "structured_rows": status.structured_rows,
            "mined_rows": status.mined_rows,
            "cluster_template_rows": status.cluster_template_rows,
        }

    @app.get("/retrieval/bm25/search")
    def bm25_search(q: str, top_k: int = 5) -> dict[str, object]:
        from logrca.retrieval import build_hdfs_2k_bm25_index, search_bm25

        index, bm25 = build_hdfs_2k_bm25_index()
        result = search_bm25(index, bm25, q, top_k=top_k)
        return {
            "query": result.query,
            "hits": [
                {
                    "record_id": hit.record_id,
                    "score": hit.score,
                    "text": hit.text,
                    "source_file": hit.source_file,
                    "cluster_id": hit.cluster_id,
                    "event_id": hit.event_id,
                    "metadata": hit.metadata,
                }
                for hit in result.hits
            ],
        }

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "LogRCA API is running"}

    return app


app = create_app()
