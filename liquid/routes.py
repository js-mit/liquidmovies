from flask import render_template, request, redirect, url_for
from flask import current_app as app
from .database import db_session, init_db
from .models import LiquidMethod, Liquid, Video


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


@app.route("/video/<int:video_id>/method/<int:liquid_id>")
def liquid_video(video_id, liquid_id):
    video = Video.query.filter(Video.id == video_id, Video.active == True).first()
    liquid = Liquid.query.filter(Liquid.id == liquid_id, Liquid.active == True).first()
    if video is None or liquid is None:
        abort(404)
    return render_template("liquid_video.html", video=video, liquid=liquid)


@app.route("/bookmarker/<int:video_id>", methods=["GET", "POST"])
def bookmarker(video_id):
    if request.method == "POST":
        bookmarks = request.form.get("bookmarks")
        desc = request.form.get("desc")
        liquid = Liquid(video=video_id, liquid=bookmarks, method=1, desc=desc)
        db_session.add(liquid)
        db_session.commit()
        return url_for("index")
    else:
        video = Video.query.filter(Video.id == video_id, Video.active == True).first()
        if video is None:
            abort(404)
        return render_template("bookmarker.html", video=video)


@app.route("/diarization/<int:video_id>", methods=["POST"])
def diarization(video_id):
    bookmarks = request.form.get("bookmarks")
    desc = request.form.get("desc")
    liquid = Liquid(video=video_id, liquid=bookmarks, method=2, desc=desc)
    db_session.add(liquid)
    db_session.commit()
    return "ok"


@app.route("/diarization/labels/<int:video_id>/<int:liquid_id>", methods=["POST"])
def diarization_labels(video_id, liquid_id):
    pass


@app.route("/liquid/delete/<int:liquid_id>")
def delete_liquid(liquid_id):
    liquid = Liquid.query.filter(Liquid.id == liquid_id).first()
    liquid.active = False
    db_session.add(liquid)
    db_session.commit()
    return redirect(url_for("index"))
