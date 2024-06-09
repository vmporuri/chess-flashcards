from src.app import create_app, db
from src.routes import register_routes

app = create_app()
register_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
