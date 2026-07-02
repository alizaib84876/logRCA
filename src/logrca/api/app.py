from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="LogRCA", version="0.1.0")

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "LogRCA API is running"}

    return app


app = create_app()
