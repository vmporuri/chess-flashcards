from src.app import create_app, db
from src.db import update_puzzle_registries

app = create_app()


@app.cli.command()
def create_db():
    """Creates tables in database if they don't already exist."""
    db.create_all()


@app.cli.command()
def refresh_puzzles():
    """Generates puzzles from new games played by users."""
    update_puzzle_registries()


if __name__ == "__main__":
    app.run(debug=True)
