import json
from app import server


def test_health():
    assert "ok" == server.health()


def test_empty_users():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.get("/users")
            assert 200 == response.status_code

            assert [] == json.loads(response.data)


def test_add_users():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.post("/users", json={"name": "sanu"})
            assert 200 == response.status_code
            response_data = response.get_json()
            assert "id" in response_data
            c.delete(f"/users/{response_data['id']}")
