from __future__ import annotations

import os

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, SubmitField
from wtforms.validators import AnyOf, DataRequired, Email

_valid_ids = os.getenv("ADMINS", "")

VALID_IDS = _valid_ids.split("|")


class AdminLogin(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    login_as = SelectField("Login As", validators=[DataRequired(), AnyOf(VALID_IDS)], choices=[(i, i) for i in VALID_IDS])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Login")
