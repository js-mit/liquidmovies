from pathlib import Path
from flask import render_template, redirect, url_for, abort, flash
from flask import current_app as app
from flask_login import current_user, login_required
import json

from . import s3
from .db import db_session
from .models import Liquid, Video, Treatment
from .forms import UploadVideoForm
from .rekognition import VideoDetector, VideoSubmitter
from .treatment import render_data
from .tasks import process_job_data


@app.route("/liquid/<int:liquid_id>")
def liquid(liquid_id):
    """ Get Liquid Video based on liquid id

    1. Download liquid data from s3 bucket
    2. Process data based on treatment type
    3. Render page with data
    """
    liquid = Liquid.query.filter(Liquid.id == liquid_id, Liquid.active == True).first()

    if liquid is None:
        abort(404)

    data = s3.download_liquid_by_url(liquid.url)
    data = render_data(data, liquid.treatment_id)

    return render_template("liquid.html", liquid=liquid, data=data)


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

    # get results from rekognition
    if not detector.get_results():

        # kickoff celery job
        process_job_data.apply_async(args=[detector.labels, job_id])
        flash(f"Job <{job_id}> results are being processed in the background...")

        # # get Liquid entry
        # path = s3.get_s3_liquid_path(current_user.id, liquid.video.id, liquid.id)
        # key = f"{path}/data.json"

        # # preprocess data depending on treatment_id
        # preprocess_data(detector.labels, liquid, liquid.treatment_id)

        # # update liquid entry
        # liquid.processing = False
        # liquid.url = s3.get_object_url(key)
        # liquid.duration = detector.duration
        # db_session.add(liquid)
        # db_session.commit()

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

        # create video entry
        video = Video(name=form.name.data, desc=form.desc.data)
        db_session.add(video)
        db_session.commit()

        # get video id to use in s3_path
        s3_path = s3.get_s3_video_path(current_user.id, video.id)

        # upload video
        success = s3.upload_fileobj(
            obj=form.video.data,
            key=f"{s3_path}/video.mp4",
            content_type="video/mp4",
        )
        if not success:
            flash("Upload Video failed.")

        # upload poster, modify depending on suffix
        ext = Path(form.poster.data.filename).suffix
        ext = "png" if "png" in ext else "jpeg"
        success = s3.upload_fileobj(
            obj=form.poster.data,
            key=f"{s3_path}/poster.{ext}",
            content_type="image/{ext}",
        )
        if not success:
            flash("Upload poster failed.")

        # update video entry with url/poster_url
        video.url = s3.get_object_url(f"{s3_path}/video.mp4")
        video.poster_url = s3.get_object_url(f"{s3_path}/poster.{ext}")
        db_session.add(video)

        # create liquid entry
        liquid = Liquid(
            video_id=video.id,
            user_id=current_user.id,
            treatment_id=form.treatment_id.data,
            active=True,
            private=form.private.data,
            processing=True,
        )
        db_session.add(liquid)
        db_session.commit()

        # submit video to aws rekognition
        submitter = VideoSubmitter(
            role_arn=app.config["AWS_REK_SERVICE_ROLE_ARN"],
            sns_topic_arn=app.config["AWS_SNS_TOPIC_ARN"],
            lambda_arn=app.config["AWS_LAMBDA_FUNCTION_ARN"],
            bucket=app.config["AWS_S3_BUCKET"],
            video=f"{s3_path}/video.mp4",
            treatment_id=form.treatment_id.data,
        )
        submitter.do_label_detection()

        # update Liquid with job id
        liquid.job_id = submitter.job_id
        db_session.add(liquid)
        db_session.commit()

        flash(f"Your video '{form.name.data}' has been successfully uploaded.")
        return redirect(url_for("profile"))

    return render_template("upload.html", form=form)
