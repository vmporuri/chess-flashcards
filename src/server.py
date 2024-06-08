from datetime import timedelta

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, request, session, url_for

from src.download import download_chess_games
from src.models import db
from src.db import register_new_user, bcrypt, USER_EXISTS

LICHESS_HOST = "https://lichess.org"

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="../static/",
    template_folder="../templates//",
)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=1)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
app.config["SQLALCHEMY_ECHO"] = True
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

oauth = OAuth(app)
oauth.register("lichess", client_kwargs={"code_challenge_method": "S256"})


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/puzzles")
def puzzles():
    return render_template("puzzle-page.html")


@app.get("/get-fen")
def get_fen():
    return {"fen": "r1k4r/p2nb1p1/2b4p/1p1n1p2/2PP4/3Q1NB1/1P3PPP/R5K1 b - - 0 19"}


@app.post("/validate-move")
def validate_move():
    body = request.json
    return {"isValidMove": body["move"] == "d5e3"}


@app.get("/authorize")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri)


@app.get("/token")
def authorize():
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
    return render_template("login.html")


@app.post("/login")
def login_post():
    user_data = dict(request.form)
    session.permanent = True
    raise NotImplementedError()


@app.get("/register")
def register_get():
    return render_template("register.html")


@app.post("/register")
def register_post():
    user_data = dict(request.form)
    user_id = register_new_user(user_data)
    if user_id == USER_EXISTS:
        return redirect("/register")
    session["user_id"] = user_id
    return redirect("/profile")


@app.get("/logout")
def logout():
    # session.pop("name", None)
    return redirect("/")


@app.get("/profile")
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
