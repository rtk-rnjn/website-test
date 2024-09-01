from flask import render_template

from src import app


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html", title="Home")


@app.route("/resources/universal-ide", methods=["GET"])
def universal_ide() -> str:
    return render_template(template_name_or_list="ide.html", title="IDE")
