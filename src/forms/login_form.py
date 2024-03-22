from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField("Email or Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Login")
