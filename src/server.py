from flask import Flask, render_template, request

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="../static/",
    template_folder="../views/",
)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 300


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/puzzles")
def puzzles():
    return render_template("puzzle-page.html")


@app.get("/get-fen")
def get_fen():
    return {"fen": "r1k4r/p2nb1p1/2b4p/1p1n1p2/2PP4/3Q1NB1/1P3PPP/R5K1 b - - 0 19"}


@app.post("/validate-move")
def validate_move():
    response = {}
    body = request.get_json()
    response["isValidMove"] = body["move"] == "d5e3"
    return response


if __name__ == "__main__":
    app.run()
