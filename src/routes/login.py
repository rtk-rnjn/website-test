from __future__ import annotations

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash

from src import app
from src.forms import LoginForm
from src.models import User


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        db = app.mongo["users_database"]
        entity = db.users.find_one({"email": email})
        if entity is None:
            return "<h1>Invalid email or password</h1>"

        password_hash = entity["password_hash"]
        if check_password_hash(password_hash, form.password.data):
            user = User()
            user.email = email
            login_user(user, remember=True)

            return redirect(url_for("protected"))

        return "<h1>Invalid email or password</h1>"

    return render_template("login.html", form=form)


@app.route("/protected")
@login_required
def protected():
    assert current_user.is_authenticated  # This is a proxy for the login_required decorator
    assert isinstance(current_user, User)

    return "Logged in as: " + current_user.email
