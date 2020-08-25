import json
from app import server


def test_health():
    assert "ok" == server.health()


def test_empty_users():
    with server.app.app_context():
        server.migrate()

        response = server.users()
        assert 200 == response.status_code

        assert [] == json.loads(response.data)
