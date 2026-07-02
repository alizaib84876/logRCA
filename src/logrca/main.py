from logrca.api.app import app


def main() -> None:
    try:
        import uvicorn
    except ImportError as exc:  # pragma: no cover - runtime convenience only
        raise SystemExit(
            "uvicorn is not installed yet. Install the API extras to run the server."
        ) from exc

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
