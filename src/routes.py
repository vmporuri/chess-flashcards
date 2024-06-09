from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from src.auth import register_new_user, verify_login_credentials

oauth = OAuth()
login_manager = LoginManager()


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect("/profile")
        return render_template("index.html")

    @app.get("/puzzles")
    @login_required
    def puzzles():
        return render_template("puzzle-page.html")

    @app.get("/get-fen")
    @login_required
    def get_fen():
        return {"fen": "r1k4r/p2nb1p1/2b4p/1p1n1p2/2PP4/3Q1NB1/1P3PPP/R5K1 b - - 0 19"}

    @app.post("/validate-move")
    @login_required
    def validate_move():
        body = request.json
        return {"isValidMove": body["move"] == "d5e3"}

    @app.get("/authorize")
    def authorize():
        redirect_uri = url_for("token", _external=True)
        return oauth.lichess.authorize_redirect(redirect_uri)

    @app.get("/token")
    def token():
        token = oauth.lichess.authorize_access_token()
        resp = oauth.lichess.get("https://lichess.org/api/account")
        resp.raise_for_status()
        body = resp.json()

        lichess_user = {}
        lichess_user["lichess_username"] = body["username"]
        lichess_user["token"] = token["access_token"]
        lichess_user["expires"] = token["expires_at"]
        lichess_user["user_id"] = current_user.user_id
        print(lichess_user)
        return redirect("/sync-games")

    @app.get("/sync-games")
    def sync_games():
        # download_chess_games(body["username"], headers)
        return redirect("/profile")

    @app.get("/login")
    def login_get():
        if current_user.is_authenticated:
            return redirect("/profile")
        return render_template("login.html")

    @app.post("/login")
    def login_post():
        user = verify_login_credentials(**request.form)
        if user is None:
            return redirect("/profile")
        login_user(user)
        return redirect("/profile")

    @app.get("/register")
    def register_get():
        if current_user.is_authenticated:
            return redirect("/profile")
        return render_template("register.html")

    @app.post("/register")
    def register_post():
        user = register_new_user(**request.form)
        if user is None:
            return redirect("/register")
        login_user(user)
        return redirect("/profile")

    @app.get("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.get("/profile")
    @login_required
    def profile():
        return render_template("profile.html")
