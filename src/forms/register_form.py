from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src import app

class RegisterForm(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=32)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm_password")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    register = SubmitField("Register")

    def validate_username(self, username: str) -> bool:
        return app.mongo.users_database.users.find_one({"username": username}) is None
