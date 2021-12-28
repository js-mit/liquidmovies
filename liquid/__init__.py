import os
from flask import Flask
from flask_login import LoginManager
# from flask_mail import Mail
from celery import Celery
from config import Config


login_manager = LoginManager()

# instantiate celery
celery = Celery(
    __name__,
    broker=Config.CELERY_BROKER_URL,
    result_backend=Config.RESULT_BACKEND
)

# # instantiate flask mail
# mail = Mail()


# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
# 
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
# 
#     celery.Task = ContextTask
#     return celery


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

    # set up celery
    celery.conf.update(app.config)

    with app.app_context():
        # Import parts of our application
        from . import routes
        from . import models
        from . import jinja_filters
        from . import auth
        from . import s3
        from . import liquid
        # from . import tasks

        return app
