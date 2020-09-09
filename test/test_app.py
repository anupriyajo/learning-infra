import pytest

from app import server

client = server.app.asgi_client


@pytest.yield_fixture
def sanic_app():
    yield server.app


@pytest.fixture
def client(loop, sanic_app, sanic_client):
    return loop.run_until_complete(sanic_client(server.app))


async def test_health(client):
    response = await client.get("/")
    assert {"message": "ok"} == await response.json()


async def test_empty_users(client):
    response = await client.get("/users")
    assert 200 == response.status
    assert [] == await response.json()
    await server.migrate(down=True)


async def test_add_users(client):
    response = await client.post("/users", json={"name": "sanu"})
    assert 200 == response.status
    response_data = await response.json()
    assert "id" in response_data
    await client.delete(f"/users/{response_data['id']}")
    await server.migrate(down=True)


async def test_add_users_failure(client):
    response = await client.post("/users", json={"manu": "sanu"})
    assert 400 == response.status
    response_data = await response.json()
    assert "error" in response_data
    assert "id" not in response_data
    await server.migrate(down=True)


async def test_delete_non_existent_users(client):
    response = await client.delete("/users/1")
    assert 404 == response.status
    response_data = await response.json()
    assert "error" in response_data
    assert "user not found" == response_data["error"]
    await server.migrate(down=True)


async def test_delete_existing_users(client):
    response = await client.post("/users", json={"name": "sanu"})
    id = (await response.json())["id"]
    response = await client.delete(f"/users/{id}")
    assert 200 == response.status
    response_data = await response.json()
    assert "id" in response_data
    assert id == response_data["id"]
    await server.migrate(down=True)


async def test_delete_error(client):
    await server.migrate(down=True)
    response = await client.delete("/users/1")
    assert 500 == response.status
    assert "error" in await response.json()
