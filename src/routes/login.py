from __future__ import annotations

from flask import redirect, render_template, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from src import app
from src.forms import LoginForm
from src.models import User


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        entity = app.mongo.users_database.users.find_one(
            {
                "$or": [
                    {"email": email},
                    {"username": email},
                ],
            },
        )
        if entity is None:
            return "<h1>Invalid email or password</h1>"

        password_hash = entity["password_hash"]
        assert form.password.data and email

        if check_password_hash(password_hash, form.password.data):
            user = User()
            user.email = email
            login_user(user, remember=True)

            return redirect(url_for("home"))

        return "<h1>Invalid email or password</h1>"

    return render_template("login.html", form=form)
