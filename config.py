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
    AWS_S3_BUCKET = "liquidmovies"
    AWS_SNS_TOPIC_ARN = os.environ.get("AWS_SNS_TOPIC_ARN")
    AWS_LAMBDA_FUNCTION_ARN = os.environ.get("AWS_LAMBDA_FUNCTION_ARN")
    AWS_REK_SERVICE_ROLE_ARN = os.environ.get("AWS_REK_SERVICE_ROLE_ARN")


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
