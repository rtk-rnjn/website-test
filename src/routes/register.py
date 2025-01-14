from __future__ import annotations

from flask import render_template, url_for
from werkzeug.security import generate_password_hash

from src import app, mongo_client as mongo
from src.forms import RegisterForm


@app.route("/register", methods=["GET", "POST"])
@app.route("/register/", methods=["GET", "POST"])
def register():
    form: RegisterForm = RegisterForm()
    if form.validate_on_submit():
        db = mongo["users_database"]
        email = form.email.data

        if db.users.find_one({"email": email}) is not None:
            return render_template(
                "register.html",
                form=form,
                error="User already exists",
            )

        assert form.password.data

        password_hash = generate_password_hash(form.password.data)
        fullname = form.fullname.data

        db.users.insert_one(
            {"email": email, "password_hash": password_hash, "fullname": fullname, "username": form.username.data},
        )

        anchor = f"<a href='{url_for('login')}'>Click here to login</a>"
        return render_template(
            "register.html",
            form=form,
            message=f"User registered successfully. {anchor}",
        )

    return render_template("register.html", form=form)
