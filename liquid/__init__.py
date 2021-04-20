import os
from flask import Flask, render_template
from werkzeug.exceptions import abort
from . import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "liquid.sqlite"),
    )

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

    @app.route("/")
    def index():
        conn = db.get_db()
        vids = conn.execute("SELECT * FROM video").fetchall()
        conn.close()
        return render_template("index.html", vids=vids)

    @app.route("/video/<int:video_id>")
    def video(video_id):
        conn = db.get_db()
        video = conn.execute("SELECT * FROM video WHERE id = ?", (video_id,)).fetchone()
        liquids = conn.execute("SELECT id, method, desc FROM liquid WHERE video = ?", (video_id,)).fetchall()
        liquids = [{"id": l["id"], "method": l["method"], "desc": l["desc"]} for l in liquids]
        conn.close()
        if video is None:
            abort(404)
        return render_template("video.html", video=video, liquids=liquids)

    @app.route("/bookmarker/<int:video_id>")
    def bookmarker(video_id):
        conn = db.get_db()
        video = conn.execute("SELECT * FROM video WHERE id = ?", (video_id,)).fetchone()
        conn.close()
        if video is None:
            abort(404)
        return render_template("bookmarker.html", video=video)

    db.init_app(app)

    return app
