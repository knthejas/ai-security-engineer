from ai_security_engineer.api.routes.health import health_check


def test_health_check_returns_ok() -> None:
    assert health_check() == {"status": "ok"}
