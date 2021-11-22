import os
from pathlib import Path
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "..", ".env"))


# use DATABASE_URL if available
# otherwise default to a local instance of a sqlite db
db_path = (
    os.environ.get("DATABASE_URL")
    if "DATABASE_URL" in os.environ
    else "sqlite:///" + str(Path(__file__).parent.parent / "instance/liquid.db")
)

engine = create_engine(f"{db_path}", convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
if "postgres" in db_path:
    Base.metadata.schema = "public"
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models

    Base.metadata.create_all(bind=engine)
