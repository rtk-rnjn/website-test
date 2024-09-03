from flask import render_template
from flask_login import current_user

from src import app


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html", title="Home", current_user=current_user)


@app.route("/resources/universal-ide", methods=["GET"])
def universal_ide() -> str:
    return render_template(template_name_or_list="ide.html", title="IDE", current_user=current_user)
