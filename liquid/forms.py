"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    InputRequired,
)


class UploadVideoForm(FlaskForm):
    """Upload Video Form."""

    name = StringField(
        "Name",
        validators=[Length(min=3), DataRequired()],
    )
    poster = FileField(
        "Poster",
        validators=[
            FileRequired("Poster file was empty!"),
            FileAllowed(["png", "jpg"], "Wrong format. Must be .png or .jpg"),
        ],
    )
    desc = TextAreaField(
        "Description",
        validators=[Optional()],
    )
    video = FileField(
        "Video",
        validators=[
            FileRequired("Video file was empty!"),
            FileAllowed(["mp4"], "Wrong format. Must be .mp4"),
        ],
    )
    treatment_id = SelectField(
        "Treatment",
        coerce=int,
        choices=[InputRequired()],
    )
    private = BooleanField(
        "Private?",
        validators=[],
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
