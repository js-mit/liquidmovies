import json
from pathlib import Path
from flask import render_template, request, redirect, url_for, abort, flash
from flask import current_app as app
from flask_login import current_user, login_required
from .db import db_session
from .models import Controller, Liquid, Video, Treatment
from .forms import UploadVideoForm
from .aws import upload_file


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
        video = form.video.data
        success = upload_file(
            file_obj=form.video.data,
            bucket=app.config["AWS_S3_BUCKET"],
            path=f"{current_user.id}/{form.name.data}",
            content_type="video/mp4",
            ext="mp4",
            object_name="video",
        )
        if not success:
            flash("Upload Video failed.")

        ext = Path(form.poster.data.filename).suffix
        ext = "png" if "png" in ext else "jpeg"
        success = upload_file(
            file_obj=form.poster.data,
            bucket=app.config["AWS_S3_BUCKET"],
            path=f"{current_user.id}/{form.name.data}",
            content_type="image/{ext}",
            ext=ext,
            object_name="poster",
        )
        if not success:
            flash("Upload poster failed.")

        video_url = f"https://{app.config['AWS_S3_BUCKET']}.s3.amazonaws.com/{current_user.id}/{form.name.data}/video.mp4"
        poster_url = f"https://{app.config['AWS_S3_BUCKET']}.s3.amazonaws.com/{current_user.id}/{form.name.data}/poster.{ext}"
        v = Video(
            url=video_url, name=form.name.data, poster=poster_url, desc=form.desc.data
        )
        db_session.add(v)
        db_session.commit()
        l = Liquid(
            video_id=v.id,
            user_id=current_user.id,
            liquid=None,
            treatment_id=form.treatment_id.data,
            active=True,
            private=form.private.data,
        )
        db_session.add(l)
        db_session.commit()
        flash("Your video <VIDEO> has been successfully uploaded.")
        return redirect(url_for("profile"))

    return render_template("upload.html", form=form)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
