from flask import redirect, url_for
from flask_login import logout_user

from src import app


@app.route("/logout", methods=["GET", "POST"])
@app.route("/logout/", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))
