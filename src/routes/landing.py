from flask import redirect, render_template, url_for
from flask_login import current_user

from src import app


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html", title="Home", current_user=current_user)


@app.route("/home", methods=["GET"])
def home():
    return redirect(url_for("index"))


@app.route("/resources/universal-ide", methods=["GET"])
def universal_ide() -> str:
    return render_template(template_name_or_list="ide.html", title="IDE", current_user=current_user)
