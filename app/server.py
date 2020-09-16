import os
import asyncpg
from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)
# TODO: share the db connection pool and run migration only once at start of server
migrations = [
    {
        "up": """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );
    """,
        "down": "DROP TABLE IF EXISTS users;",
    }
]

db_user = os.environ.get("DB_USER", "py")
db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", "5432")
db_password = os.environ.get("DB_PASSWORD", "password")
db_name = os.environ.get("DB_NAME", "users")


async def migrate(down=False):
    for migration in map(lambda m: m["down"] if down else m["up"], migrations):
        print(f"Running migration: {migration}")
        await app.conn.execute(migration)


@app.listener("before_server_start")
async def setup_server(app, loop):
    conn = await asyncpg.connect(
        f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}?password={db_password}"
    )
    app.conn = conn
    await migrate()


@app.listener("after_server_stop")
async def teardown_server(app, loop):
    await app.conn.close()


@app.route("/", methods=["GET"])
async def health(request):
    return json({"message": "ok"})


@app.route("/users", methods=["GET"])
async def users(request):
    sql = "SELECT * FROM users"
    results = await app.conn.fetch(sql)
    users = list(
        map(lambda result: {"id": result["id"], "name": result["name"]}, results)
    )

    return json(users)


@app.route("/users", methods=["POST"])
async def add_users(request):
    sql = """INSERT INTO users(name)
             VALUES($1) RETURNING id;"""
    try:
        result = await app.conn.fetchrow(sql, request.json["name"])
    except Exception as error:
        print(f"failed to save user: {error}")
        return json({"error": str(error)}, status=400)

    return json({"id": result["id"]})


@app.route("/users/<id>", methods=["DELETE"])
async def delete_users(request, id):
    sql = "DELETE FROM users WHERE id=$1 RETURNING id"
    try:
        result = await app.conn.fetchrow(sql, int(id))
        if not result:
            return json({"error": "user not found"}, status=404)
    except Exception as error:
        print(f"failed to delete user: {error}")
        return json({"error": str(error)}, status=500)
    return json({"id": result["id"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, workers=os.cpu_count() + 1)

# change the hardcode of port
# change docker file entryoint
# make the infra
