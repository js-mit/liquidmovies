from flask import current_app as app
from flask_login import login_required, logout_user, current_user, login_user
from flask import render_template, request, redirect, url_for, abort, flash, session
from .forms import SignupForm, LoginForm
from .db import db_session
from .models import User
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db_session.add(user)
            db_session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for("profile"))
        flash("A user already exists with that email address.")
    return render_template(
        "signup.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("profile"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        flash("Invalid username/password combination")
        return redirect(url_for("login"))
    return render_template(
        "login.html",
        form=form,
        title="Log in.",
        template="login-page",
        body="Log in with your User account.",
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    Arugs:
    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)