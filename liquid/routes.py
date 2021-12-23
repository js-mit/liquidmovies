from flask import render_template, abort
from flask import current_app as app
from flask_login import current_user, login_required

from . import s3
from .db import db_session
from .models import Liquid, Video


@app.route("/")
def index():
    if current_user.is_authenticated:
        print(current_user.id)

    liquids = Liquid.query.filter(
        (Liquid.active == True),
        (Liquid.private == False),
    ).all()
    return render_template("index.html", liquids=liquids)


@app.route("/profile")
@login_required
def profile():
    liquids = Liquid.query.filter(
        (Liquid.active == True),
        (Liquid.user_id == current_user.id),
    ).all()

    # testing only
    l = Liquid.query.get(7)
    data = s3.get_liquid_data(current_user.id, l.video.id, l.id)

    return render_template("profile.html", liquids=liquids)


@app.route("/video/<int:video_id>")
def raw_video(video_id):
    video = Video.query.filter(Video.id == video_id, Video.active == True).first()
    if video is None:
        abort(404)
    return render_template("raw_video.html", video=video)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
