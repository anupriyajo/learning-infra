import os

import flask
import psycopg2
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

migrations = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
]


def connect():
    try:
        env = os.environ
        return psycopg2.connect(
            user=env.get("DB_USER", "py"),
            password=env.get("DB_PASSWORD", "password"),
            host=env.get("DB_HOST", "127.0.0.1"),
            port=env.get("DB_PORT", "5432"),
            database=env.get("DB_NAME", "users"),
        )
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def migrate():
    conn = connect()

    cur = conn.cursor()
    for migration in migrations:
        print(f"Running migration: {migration}")
        cur.execute(migration)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/", methods=["GET"])
def health():
    return "ok"


@app.route("/users", methods=["GET"])
def users():
    sql = "SELECT * FROM users"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    users = list(map(lambda result: {"id": result[0], "name": result[1]}, results))

    cur.close()
    conn.close()

    return jsonify(users)


@app.route("/users", methods=["POST"])
def add_users():
    sql = """INSERT INTO users(name)
             VALUES(%s) RETURNING id;"""
    try:
        conn = connect()
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (request.json["name"],))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except Exception as error:
        print(f"failed to save user: {error}")
        return jsonify({"error": str(error)}), 400
    finally:
        conn.close()

    return jsonify({"id": id})


@app.route("/users/<id>", methods=["DELETE"])
def delete_users(id):
    sql = "DELETE FROM users WHERE id=%s RETURNING id"
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (int(id),))
        id = cur.fetchone()
        if not id:
            return jsonify({"error": "user not found"}), 404
        conn.commit()
        cur.close()
    except Exception as error:
        print(f"failed to delete user: {error}")
        return jsonify({"error": str(error)}), 500
    finally:
        conn.close()

    return jsonify({"id": id})


if __name__ == "__main__":
    migrate()
    app.run("0.0.0.0", 5000)
