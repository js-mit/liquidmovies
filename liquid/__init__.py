import os
from flask import Flask
from flask_login import LoginManager
from celery import Celery
from config import Config


login_manager = LoginManager()

# instantiate celery
celery = Celery(
    __name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.RESULT_BACKEND
)


def create_app(test_config=None):
    """Main application that uses the Flask factory pattern."""

    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object("config.Prod")
    else:
        # load the test config if passed in
        app.config.from_object("config.Dev")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init plugins
    login_manager.init_app(app)

    # set up celery
    celery.conf.update(app.config)

    with app.app_context():
        # Import parts of our application
        from . import routes
        from . import models
        from . import jinja_filters
        from . import auth
        from . import s3
        from . import rekognition
        from . import liquid

        return app
