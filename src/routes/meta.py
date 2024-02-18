from flask import render_template

from src import app
import json

@app.route("/")
def index() -> str:
    return render_template("index.html", title="Index")


@app.route("/resources/universal_ide")
def universal_ide() -> str:
    return render_template(template_name_or_list="ide.html", title="IDE")


with open("python.json") as f:
    questions = json.load(f)

@app.route("/test")
def test() -> str:
    return render_template("mcq.html", title="Test", questions=questions)