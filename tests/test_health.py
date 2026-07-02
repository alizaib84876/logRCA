from logrca.api.app import app


def test_health_route_exists() -> None:
    paths = {route.path for route in app.routes}
    assert "/health" in paths
