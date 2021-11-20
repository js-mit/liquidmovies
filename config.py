"""Flask configuration."""
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class Prod(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class Dev(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
