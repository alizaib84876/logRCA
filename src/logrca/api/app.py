from fastapi import FastAPI

from logrca.ingestion import build_hdfs_2k_ingestion_status


def create_app() -> FastAPI:
    app = FastAPI(title="LogRCA", version="0.1.0")

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ingestion/hdfs-2k/status")
    def hdfs_2k_status() -> dict[str, int | str | bool]:
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

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "LogRCA API is running"}

    return app


app = create_app()
