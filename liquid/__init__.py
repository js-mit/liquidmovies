import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.exceptions import abort
from .database import db_session, init_db
from .models import LiquidMethod, Liquid, Video


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # routes
    @app.route("/")
    def index():
        videos = Video.query.filter(Video.active==True).all()
        liquids = Liquid.query.filter(Liquid.active==True).all()
        return render_template("index.html", videos=videos, liquids=liquids)

    @app.route("/video/<int:video_id>")
    def raw_video(video_id):
        video = Video.query.filter(Video.id==video_id, Video.active==True).first()
        if video is None:
            abort(404)
        return render_template("raw_video.html", video=video)

    @app.route("/video/<int:video_id>/method/<int:liquid_id>")
    def liquid_video(video_id, liquid_id):
        video = Video.query.filter(Video.id==video_id, Video.active==True).first()
        liquid = Liquid.query.filter(Liquid.id==liquid_id, Liquid.active==True).first()
        if video is None or liquid is None:
            abort(404)
        return render_template("liquid_video.html", video=video, liquid=liquid)

    @app.route("/bookmarker/<int:video_id>", methods=['GET', 'POST'])
    def bookmarker(video_id):
        if request.method=="POST":
            bookmark = request.form.get("bookmarks")
            liquid = Liquid(video=video_id, liquid=bookmark, method=1, desc="generated from webapp")
            db_session.add(liquid)
            db_session.commit()
            return url_for('index')
        else:
            video = Video.query.filter(Video.id==video_id, Video.active==True).first()
            if video is None:
                abort(404)
            return render_template("bookmarker.html", video=video)

    @app.route("/liquid/delete/<int:liquid_id>")
    def delete_liquid(liquid_id):
        liquid = Liquid.query.filter(Liquid.id==liquid_id).first()
        liquid.active = False
        db_session.add(liquid)
        db_session.commit()
        return redirect(url_for('index'))

    return app
