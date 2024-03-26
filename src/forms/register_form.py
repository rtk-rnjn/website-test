from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src import app


class RegisterForm(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=32)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), EqualTo("confirm_password"), Length(min=8)],
        description="Password must be at least 8 characters long",
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password"), Length(min=8)],
        description="Passwords must match",
    )

    register = SubmitField("Register")

    def validate_username(self, username: StringField) -> bool:
        return app.mongo.users_database.users.find_one({"username": username.data}) is None

    def validate_email(self, email: EmailField) -> bool:
        return app.mongo.users_database.users.find_one({"email": email.data}) is None
