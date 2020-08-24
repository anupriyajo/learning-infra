from app.server import app, migrate

migrate()

if __name__ == "__main__":
    app.run()
