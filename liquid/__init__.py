import os
from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()


def create_app(test_config=None):
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

    with app.app_context():
        # Import parts of our application
        from . import routes
        from . import models
        from . import jinja_filters
        from . import auth
        from . import aws
        from . import liquid

        return app
