from __future__ import annotations

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user

from src import app
from src.forms import LoginForm
from src.models import User

users: dict[str, dict[str, str]] = {"email@domain.com": {"password": "password"}}


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        if form.password.data == users[email]["password"]:
            user = User()
            user.email = email
            login_user(user)
            return redirect(url_for("protected"))

        return "<h1>Invalid email or password</h1>"

    return render_template("login.html", form=form)


@app.route("/protected")
@login_required
def protected():
    return "Logged in as: " + current_user.email
