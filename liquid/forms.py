"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL


class UploadVideoForm(FlaskForm):
    """Upload Video Form."""

    name = StringField(
        "Name",
        validators=[Length(min=3), DataRequired()],
    )
    poster = FileField(
        "Poster",
        validators=[FileRequired("File was empty!")],
    )
    private = BooleanField(
        "Private?",
        validators=[DataRequired()],
    )
    url = StringField(
        "Video URL",
        validators=[
            URL(True, "Invalid URL"),
            DataRequired(),
        ]
    )
    submit = SubmitField("Upload")


class SignupForm(FlaskForm):
    """User Sign-up Form."""

    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """User Log-in Form."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
