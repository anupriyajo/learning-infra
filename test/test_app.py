from app import server


def test_health():
    assert "ok" == server.health()


def test_empty_users():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.get("/users")
            assert 200 == response.status_code

            assert [] == response.get_json()

        server.migrate(down=True)


def test_add_users():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.post("/users", json={"name": "sanu"})
            assert 200 == response.status_code
            response_data = response.get_json()
            assert "id" in response_data
            c.delete(f"/users/{response_data['id']}")

        server.migrate(down=True)


def test_add_users_failure():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.post("/users", json={"manu": "sanu"})
            assert 400 == response.status_code
            response_data = response.get_json()
            assert "error" in response_data
            assert "id" not in response_data

        server.migrate(down=True)


def test_delete_non_existent_users():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.delete("/users/1")
            assert 404 == response.status_code
            response_data = response.get_json()
            assert "error" in response_data
            assert "user not found" == response_data["error"]

        server.migrate(down=True)


def test_delete_existing_users():
    with server.app.app_context():
        server.migrate()

        with server.app.test_client() as c:
            response = c.post("/users", json={"name": "sanu"})
            id = response.get_json()["id"]
            response = c.delete(f"/users/{id}")
            assert 200 == response.status_code
            response_data = response.get_json()
            assert "id" in response_data
            assert id == response_data["id"]

        server.migrate(down=True)


def test_delete_error():
    with server.app.test_client() as c:
        response = c.delete("/users/1")
        assert 500 == response.status_code
        assert "error" in response.get_json()

    server.migrate(down=True)

