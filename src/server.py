from datetime import timedelta

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for
from flask_pydantic import validate
from pydantic import BaseModel, Field

from src.db import download_chess_games

LICHESS_HOST = "https://lichess.org"

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="../static/",
    template_folder="../views/",
)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=1)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)
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


oauth = OAuth(app)
oauth.register("lichess", client_kwargs={"code_challenge_method": "S256"})


class MoveModel(BaseModel):
    move: str = Field(pattern=r"^([a-h][1-8]){2}[qrbn]?$")


class ValidationModel(BaseModel):
    isValidMove: bool


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
@validate()
def validate_move(body: MoveModel):
    return ValidationModel(isValidMove=body.move == "d5e3")


@app.get("/login")
def login():
    assert oauth.lichess is not None
    redirect_uri = url_for("authorize", _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri)


@app.get("/authorize")
def authorize():
    assert oauth.lichess is not None
    token = oauth.lichess.authorize_access_token()
    resp = oauth.lichess.get(f"{LICHESS_HOST}/api/account")
    resp.raise_for_status()
    body = resp.json()
    session.permanent = True
    session["name"] = body["username"]
    bearer = token["access_token"]
    headers = {"Authorization": f"Bearer {bearer}"}
    download_chess_games(body["username"], headers)
    return redirect("/")


@app.get("/logout")
def logout():
    session.pop("name", None)
    return redirect("/")


if __name__ == "__main__":
    app.run()
