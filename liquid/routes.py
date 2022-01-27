from flask import render_template, abort
from flask import current_app as app
from flask_login import current_user, login_required

from .db import db_session
from .models import Liquid, Video
from .tasks import celery_test


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
def raw_video(video_id: int):
    video = Video.query.filter(Video.id == video_id, Video.active == True).first()
    if video is None:
        abort(404)
    return render_template("raw_video.html", video=video)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# testing celery!
@app.route("/celery")
def celery():
    celery_test.apply_async(args=["hi"])
    return "success"


# Testing transcribe
import boto3

aws_trs = boto3.client("transcribe", region_name="us-east-1")


@app.route("/subtitles_test/<job_id>")
def subtitles_test(job_id):
    print("hello,here")
    status = aws_trs.get_transcription_job(TranscriptionJobName=job_id)
    if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
        return str(status["TranscriptionJob"]["Subtitles"]["SubtitleFileUris"])
