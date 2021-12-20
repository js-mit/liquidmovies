from pathlib import Path
from flask import render_template, redirect, url_for, abort, flash
from flask import current_app as app
from flask_login import current_user, login_required
from .db import db_session
from .models import Liquid, Video, Treatment
from .forms import UploadVideoForm
from .aws import upload_file


@app.route("/liquid/<int:liquid_id>")
def liquid(liquid_id):
    """TODO"""
    liquid = Liquid.query.filter(Liquid.id == liquid_id, Liquid.active is True).first()
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

        video = Video(name=form.name.data, desc=form.desc.data)
        db_session.add(video)
        db_session.commit()

        OBJECT_PATH = f"user_content/{current_user.id}/{video.id}"

        success = upload_file(
            file_obj=form.video.data,
            bucket=app.config["AWS_S3_BUCKET"],
            path=OBJECT_PATH,
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
            path=OBJECT_PATH,
            content_type="image/{ext}",
            ext=ext,
            object_name="poster",
        )
        if not success:
            flash("Upload poster failed.")

        video.url = f"https://{app.config['AWS_S3_BUCKET']}.s3.amazonaws.com/{OBJECT_PATH}/video.mp4"
        video.poster_url = f"https://{app.config['AWS_S3_BUCKET']}.s3.amazonaws.com/{OBJECT_PATH}/poster.{ext}"
        db_session.add(video)

        liquid = Liquid(
            video_id=video.id,
            user_id=current_user.id,
            liquid=None,
            treatment_id=form.treatment_id.data,
            active=True,
            private=form.private.data,
        )
        db_session.add(liquid)
        db_session.commit()

        flash(f"Your video '{form.name.data}'has been successfully uploaded.")
        return redirect(url_for("profile"))

    return render_template("upload.html", form=form)
