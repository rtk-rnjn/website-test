from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired, FileSize
from wtforms import EmailField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email


class AdminLogin(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Login")


class QuestionUploadForm(FlaskForm):
    docx = FileField(
        "Upload Questions",
        validators=[
            FileRequired(),
            FileSize(max_size=1 * 1024 * 1024),
            FileAllowed(["docx", "doc"], "Only .docx and .doc files are allowed"),
        ],
    )
    _type = SelectField(
        "Type",
        choices=[("qa", "Quantitative Aptitude"), ("lr", "Logical Reasoning")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Upload")
