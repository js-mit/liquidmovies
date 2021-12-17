import json
from flask import render_template, request, redirect, url_for, abort, flash
from flask import current_app as app
from flask_login import current_user, login_required
from .db import db_session
from .models import Controller, Liquid, Video, Treatment
from .forms import UploadVideoForm


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
    return render_template("profile.html", liquids=liquids)


@app.route("/video/<int:video_id>")
def raw_video(video_id):
    video = Video.query.filter(Video.id == video_id, Video.active == True).first()
    if video is None:
        abort(404)
    return render_template("raw_video.html", video=video)


@app.route("/liquid/<int:liquid_id>")
def liquid(liquid_id):
    """TODO"""
    liquid = Liquid.query.filter(Liquid.id == liquid_id, Liquid.active == True).first()
    if liquid is None:
        abort(404)

    return render_template("liquid.html", liquid=liquid)


@app.route("/liquid/delete/<int:liquid_id>")
@login_required
def delete_liquid(liquid_id):
    liquid = Liquid.query.filter(Liquid.id == liquid_id).first()
    liquid.active = False
    db_session.add(liquid)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/liquid/upload", methods=["GET", "POST"])
@login_required
def upload_liquid():
    """Uploads liquid
    POST:
        1. Upload video to aws s3 and get video s3 url
        2. Create Video entry
        3. Create Liquid entry
        4. save to db
    GET:
        render upload page
    """
    form = UploadVideoForm()
    treatments = Treatment.query.all()
    treatment_options = [(treatment.id, treatment.name) for treatment in treatments]
    form.treatment_id.choices = treatment_options
    if form.validate_on_submit():
        print("VALIDATED")
        # form.video.data
        flash("Your video <VIDEO> has been successfully uploaded.")
        return redirect(url_for("profile"))

    return render_template("upload.html", form=form)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
