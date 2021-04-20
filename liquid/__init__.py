import os
from flask import Flask, render_template
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

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # routes
    @app.route("/")
    def index():
        videos = Video.query.all()
        return render_template("index.html", videos=videos)

    @app.route("/video/<int:video_id>")
    def video(video_id):
        video = Video.query.filter(Video.id == video_id).first()
        liquids = (
            Liquid.query.with_entities(Liquid.id, Liquid.method, Liquid.desc)
            .filter(video == video_id)
            .all()
        )
        if video is None:
            abort(404)
        return render_template("video.html", video=video, liquids=liquids)

    @app.route("/bookmarker/<int:video_id>")
    def bookmarker(video_id):
        video = Video.query.filter(Video.id == video_id).first()
        if video is None:
            abort(404)
        return render_template("bookmarker.html", video=video)

    return app
