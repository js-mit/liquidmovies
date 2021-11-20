import json
from flask import render_template, request, redirect, url_for, abort
from flask import current_app as app
from .db import db_session
from .models import Controller, Liquid, Video


@app.route("/")
def index():
    videos = Video.query.filter(Video.active == True).all()
    liquids = Liquid.query.filter(Liquid.active == True).all()
    return render_template("index.html", videos=videos, liquids=liquids)


@app.route("/video/<int:video_id>")
def raw_video(video_id):
    video = Video.query.filter(Video.id == video_id, Video.active == True).first()
    if video is None:
        abort(404)
    return render_template("raw_video.html", video=video)


@app.route("/video/<int:video_id>/liquid/<int:liquid_id>")
def liquid_video(video_id, liquid_id):
    video = Video.query.filter(Video.id == video_id, Video.active == True).first()
    liquid = Liquid.query.filter(Liquid.id == liquid_id, Liquid.active == True).first()
    if video is None or liquid is None:
        abort(404)
    return render_template("liquid_video.html", video=video, liquid=liquid)


@app.route("/liquid/delete/<int:liquid_id>")
def delete_liquid(liquid_id):
    liquid = Liquid.query.filter(Liquid.id == liquid_id).first()
    liquid.active = False
    db_session.add(liquid)
    db_session.commit()
    return redirect(url_for("index"))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
