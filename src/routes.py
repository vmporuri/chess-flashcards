from authlib.integrations.flask_client import OAuth
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from src.auth import add_oauth_token, register_new_user, verify_login_credentials
from src.db import add_puzzles_to_db, fetch_random_puzzle_fen

oauth = OAuth()
login_manager = LoginManager()


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        """Renders the home page."""
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        return render_template("index.html")

    @app.get("/puzzles")
    @login_required
    def puzzles():
        """Renders the puzzle page."""
        if current_user.lichess_user is None:
            return redirect(url_for("profile"))
        return render_template("puzzle-page.html")

    @app.get("/get-fen")
    @login_required
    def get_fen():
        """Retrieves a random puzzle fen from the database."""
        print(f"FEN in session: {'fen' in session}")
        if "fen" not in session or not session["fen"]:
            fen, solution = fetch_random_puzzle_fen(current_user.user_id)
            print(fen)
            session["fen"] = fen
            session["solution"] = solution
        print(session["fen"])
        return {"fen": session["fen"]}

    @app.post("/validate-move")
    @login_required
    def validate_move():
        """Validates the chess move provided in the request body."""
        body = request.json
        if is_correct := body["move"] == session["solution"]:
            session.pop("fen", None)
            session.pop("solution", None)
        return {"isValidMove": is_correct}

    @app.get("/authorize")
    @login_required
    def authorize():
        """Retrieves Lichess authorization code (via OAuth 2.0 PKCE flow)."""
        if current_user.lichess_user is not None:
            return redirect(url_for("profile"))
        redirect_uri = url_for("token", _external=True)
        return oauth.lichess.authorize_redirect(redirect_uri)

    @app.get("/token")
    @login_required
    def token():
        """Retrieves Lichess access token and adds to database."""
        token = oauth.lichess.authorize_access_token()
        resp = oauth.lichess.get("https://lichess.org/api/account")
        resp.raise_for_status()
        body = resp.json()

        add_oauth_token(
            user_id=current_user.user_id,
            lichess_username=body["username"],
            token=token["access_token"],
            expires=token["expires_at"],
        )
        add_puzzles_to_db.queue(current_user.lichess_user)
        flash("Linked account successfully!", "info")
        return redirect(url_for("profile"))

    @app.get("/login")
    def login_get():
        """Renders the login page."""
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        return render_template("login.html")

    @app.post("/login")
    def login_post():
        """Verifies the provided login credentials."""
        user = verify_login_credentials(**request.form)
        if user is None:
            flash("Incorrect Username or Password", "warning")
            return redirect(url_for("login_get"))
        login_user(user)
        return redirect(url_for("profile"))

    @app.get("/register")
    def register_get():
        """Renders the registration page."""
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        return render_template("register.html")

    @app.post("/register")
    def register_post():
        """Registers the user with the provided credentials."""
        user = register_new_user(**request.form)
        if user is None:
            flash("Username Already in Use", "warning")
            return redirect(url_for("register_get"))
        login_user(user)
        return redirect(url_for("profile"))

    @app.get("/logout")
    @login_required
    def logout():
        """Logs out the user, ending their session."""
        session.pop("fen", None)
        session.pop("solution", None)
        logout_user()
        flash("Logged out Successfully", "info")
        return redirect(url_for("index"))

    @app.get("/profile")
    @login_required
    def profile():
        """Renders the profile page."""
        return render_template("profile.html")
