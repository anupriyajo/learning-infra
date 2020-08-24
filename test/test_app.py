from app import server


def test_health():
    assert "ok" == server.health()
