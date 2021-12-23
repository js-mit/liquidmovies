from pathlib import Path
from flask import render_template, redirect, url_for, abort, flash
from flask import current_app as app
from flask_login import current_user, login_required

from . import s3
from .db import db_session
from .models import Liquid, Video, Treatment
from .forms import UploadVideoForm
from .rekognition import VideoDetector, VideoSubmitter


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


@app.route("/liquid/job/<job_id>")
@login_required
def get_liquid_job(job_id):
    """Gets job results from Rekcognition

    1. get results from Rekcognition API
    2. save json results to S3 location
    3. upload liquid entry
    """
    detector = VideoDetector(job_id)
    if not detector.get_results():
        liquid = Liquid.query.filter(Liquid.job_id == job_id).first()

        path = s3.get_s3_liquid_path(
            current_user.id, liquid.video.id, liquid.id
        )
        key = f"{path}/data.json"
        if s3.upload(
            file_obj=detector.labels,
            bucket=app.config["AWS_S3_BUCKET"],
            key=key,
            content_type="application/json",
        ):
            liquid.processing = False
            liquid.url = s3.get_object_url(key)
            liquid.duration = detector.duration
            db_session.add(liquid)
            db_session.commit()
        else:
            print("ERROR")
    return redirect(url_for("profile"))


@app.route("/liquid/upload", methods=["GET", "POST"])
@login_required
def upload_liquid():
    """Uploads video + kicks of video processing

    POST:
        1. Upload video to aws s3 and get video s3 url
        2. Create Video entry (and save to db)
        3. Create Liquid entry (and save to db)
        4. Kickoff image processing on aws
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

        s3_path = s3.get_s3_video_path(current_user.id, video.id)

        success = s3.upload(
            file_obj=form.video.data,
            bucket=app.config["AWS_S3_BUCKET"],
            key=f"{s3_path}/video.mp4",
            content_type="video/mp4",
        )
        if not success:
            flash("Upload Video failed.")

        ext = Path(form.poster.data.filename).suffix
        ext = "png" if "png" in ext else "jpeg"
        success = s3.upload(
            file_obj=form.poster.data,
            bucket=app.config["AWS_S3_BUCKET"],
            key=f"{s3_path}/poster.{ext}",
            content_type="image/{ext}",
        )
        if not success:
            flash("Upload poster failed.")

        video.url = s3.get_object_url(f"{s3_path}/video.mp4")
        video.poster_url = s3.get_object_url(f"{s3_path}/poster.{ext}")
        db_session.add(video)

        liquid = Liquid(
            video_id=video.id,
            user_id=current_user.id,
            instructions=None,
            treatment_id=form.treatment_id.data,
            active=True,
            private=form.private.data,
            processing=True,
        )
        db_session.add(liquid)
        db_session.commit()

        submitter = VideoSubmitter(
            role_arn=app.config["AWS_REK_SERVICE_ROLE_ARN"],
            sns_topic_arn=app.config["AWS_SNS_TOPIC_ARN"],
            lambda_arn=app.config["AWS_LAMBDA_FUNCTION_ARN"],
            bucket=app.config["AWS_S3_BUCKET"],
            video=f"{s3_path}/video.mp4",
            treatment_id=form.treatment_id.data,
        )
        submitter.do_label_detection()

        liquid.job_id = submitter.job_id
        db_session.add(liquid)
        db_session.commit()

        flash(f"Your video '{form.name.data}' has been successfully uploaded.")
        return redirect(url_for("profile"))

    return render_template("upload.html", form=form)
