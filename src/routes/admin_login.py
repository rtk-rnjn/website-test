from __future__ import annotations

import os

from flask import redirect, render_template, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash

from src import app
from src.forms import AdminLogin
from src.models import User

password = generate_password_hash(os.environ["ADMIN_PASSWORD"])


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    form = AdminLogin()
    if form.validate_on_submit():
        if check_password_hash(password, form.password.data):
            user = User()
            user.email = form.email.data
            user.is_admin = True

            login_user(user)

            return redirect(url_for("admin_page"))
        return "<h1>Invalid email or password</h1>"

    return render_template("admin_login.html", form=form)
