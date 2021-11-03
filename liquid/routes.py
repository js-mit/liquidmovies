import json
from flask import render_template, request, redirect, url_for, abort
from flask import current_app as app
from .database import db_session, init_db
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


# @app.route("/diarization/<int:video_id>", methods=["POST"])
# def diarization(video_id):
#     bookmarks = request.form.get("bookmarks")
#     desc = request.form.get("desc")
#     liquid = Liquid(video=video_id, liquid=bookmarks, controller=2, desc=desc)
#     db_session.add(liquid)
#     db_session.commit()
#     return "ok"
# 
# 
# @app.route("/diarization/labels/<int:video_id>/<int:liquid_id>", methods=["POST"])
# def diarization_labels(video_id, liquid_id):
#     mapping = request.form.get("mapping") # {"C": "john", "A": "tucker", "B": "john", "D": "tucker"}
#     liquid = Liquid.query.filter(Liquid.id == liquid_id).first()
# 
#     # remap liquid bookmarks
#     bookmarks = liquid.liquid
#     mapping = json.loads(mapping)
#     for key, value in mapping.items():
#         if value in bookmarks:
#             bookmarks[value].append(bookmarks.pop(key))
#         else:
#             bookmarks[value] = bookmarks.pop(key)
# 
#     # TODO check if remaining keys exist, then call error
# 
#     # update liquid entry
#     new_liquid = Liquid(video_id=video_id, liquid=bookmarks, controller_id=liquid.controller_id, desc=liquid.desc)
#     liquid_id = new_liquid.id
#     db_session.add(new_liquid)
#     db_session.commit()
# 
#     # update old liquid entry as inactive
#     liquid.active = False
#     db_session.add(liquid)
#     db_session.commit()
# 
#     return url_for("liquid_video", liquid_id=liquid_id, video_id=video_id)


@app.route("/liquid/delete/<int:liquid_id>")
def delete_liquid(liquid_id):
    liquid = Liquid.query.filter(Liquid.id == liquid_id).first()
    liquid.active = False
    db_session.add(liquid)
    db_session.commit()
    return redirect(url_for("index"))
