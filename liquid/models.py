from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    JSON,
    Text,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from .db import Base


class User(UserMixin, Base):
    """User account model."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(200), primary_key=False, unique=False, nullable=False)
    created_on = Column(
        DateTime, index=False, unique=False, nullable=False, server_default=func.now()
    )
    last_login = Column(DateTime, index=False, unique=False, nullable=True)
    videos = relationship("Video", backref="user")

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Video(Base):
    """ TODO """

    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    url = Column(String, nullable=False)
    poster = Column(String, nullable=True)
    active = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return f"<Video: {self.name} | {self.url}>"


class Liquid(Base):
    """ TODO """

    __tablename__ = "liquid"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    video_id = Column(Integer, ForeignKey("video.id"))
    liquid = Column(JSON, nullable=False)
    controller_id = Column(Integer, ForeignKey("controller.id"))
    desc = Column(Text, nullable=True)
    active = Column(Boolean, unique=False, default=True)
    controller = relationship("Controller", backref="liquids")
    video = relationship("Video", backref="liquids")

    def __repr__(self):
        return f"<Liquid: {self.id}>"


class Controller(Base):
    """ TODO """

    __tablename__ = "controller"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    # TODO delete this?
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f"<Controller: {self.name}>"
