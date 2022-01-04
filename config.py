"""Flask configuration."""
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET")
    AWS_SNS_TOPIC_ARN = os.environ.get("AWS_SNS_TOPIC_ARN")
    AWS_SQS_QUEUE_URL = os.environ.get("AWS_SQS_QUEUE_URL")
    AWS_SQS_QUEUE_ARN = os.environ.get("AWS_SQS_QUEUE_ARN")
    AWS_REK_SERVICE_ROLE_ARN = os.environ.get("AWS_REK_SERVICE_ROLE_ARN")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    RESULT_BACKEND = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")


class Prod(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class Staging(Config):
    FLASK_ENV = "development"
    DEBUG = True
    Testing = True


class Dev(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
