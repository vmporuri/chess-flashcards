from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_session import Session
from src.db import bcrypt, login_manager, register_new_user, verify_login_credentials
from src.models import db

LICHESS_HOST = "https://lichess.org"

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="../static/",
    template_folder="../templates//",
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db
app.config["SESSION_CLEANUP_N_REQUESTS"] = 100

app.config["LICHESS_AUTHORIZE_URL"] = f"{LICHESS_HOST}/oauth"
app.config["LICHESS_ACCESS_TOKEN_URL"] = f"{LICHESS_HOST}/api/token"
# NOTE: Set a secure SECRET_KEY and LICHESS_CLIENT_ID in a .env file when not
# running in a development environment. Then, replace the following lines with
# the commented out lines.
app.config["SECRET_KEY"] = "dummy-key"
app.config["LICHESS_CLIENT_ID"] = "chess-flashcards"
# import os
# from dotenv import load_dotenv
# load_dotenv("../.env")
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# app.config["LICHESS_CLIENT_ID"] = os.getenv("LICHESS_CLIENT_ID")

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
Session(app)

login_manager.login_view = "/login"

oauth = OAuth(app)
oauth.register("lichess", client_kwargs={"code_challenge_method": "S256"})


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
    redirect_uri = url_for("authorize", _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri)


@app.get("/token")
def token():
    token = oauth.lichess.authorize_access_token()
    print(token)
    resp = oauth.lichess.get(f"{LICHESS_HOST}/api/account")
    resp.raise_for_status()
    body = resp.json()
    # bearer = token["access_token"]
    # headers = {"Authorization": f"Bearer {bearer}"}
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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
