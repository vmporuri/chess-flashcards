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
from src.db import add_puzzles_to_db, fetch_random_puzzle_fen, executor

oauth = OAuth()
login_manager = LoginManager()


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        return render_template("index.html")

    @app.get("/puzzles")
    @login_required
    def puzzles():
        if current_user.lichess_user is None:
            return redirect(url_for("profile"))
        return render_template("puzzle-page.html")

    @app.get("/get-fen")
    @login_required
    def get_fen():
        if "fen" not in session or not session["fen"]:
            fen, solution = fetch_random_puzzle_fen(current_user.user_id)
            session["fen"] = fen
            session["solution"] = solution
        return {"fen": session["fen"]}

    @app.post("/validate-move")
    @login_required
    def validate_move():
        body = request.json
        if is_correct := body["move"] == session["solution"]:
            session.pop("fen", None)
            session.pop("solution", None)
        return {"isValidMove": is_correct}

    @app.get("/authorize")
    @login_required
    def authorize():
        if current_user.lichess_user is not None:
            return redirect(url_for("profile"))
        redirect_uri = url_for("token", _external=True)
        return oauth.lichess.authorize_redirect(redirect_uri)

    @app.get("/token")
    @login_required
    def token():
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
        executor.submit(add_puzzles_to_db, current_user.lichess_user)
        flash("Linked account successfully!", "info")
        return redirect(url_for("profile"))

    @app.get("/login")
    def login_get():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        return render_template("login.html")

    @app.post("/login")
    def login_post():
        user = verify_login_credentials(**request.form)
        if user is None:
            flash("Incorrect Username or Password", "warning")
            return redirect(url_for("login_get"))
        login_user(user)
        return redirect(url_for("profile"))

    @app.get("/register")
    def register_get():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        return render_template("register.html")

    @app.post("/register")
    def register_post():
        user = register_new_user(**request.form)
        if user is None:
            flash("Username Already in Use", "warning")
            return redirect(url_for("register_get"))
        login_user(user)
        return redirect(url_for("profile"))

    @app.get("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out Successfully", "info")
        return redirect(url_for("index"))

    @app.get("/profile")
    @login_required
    def profile():
        return render_template("profile.html")
