from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db import Base


class User(UserMixin, Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(200), primary_key=False, unique=False, nullable=False)
    created_on = Column(
        DateTime, index=False, unique=False, nullable=False, server_default=func.now()
    )
    last_login = Column(DateTime, index=False, unique=False, nullable=True)

    liquids = relationship("Liquid", backref="user")

    def set_password(self, password: str):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password: str) -> bool:
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return "<User {}>".format(self.email)


class Video(Base):

    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    desc = Column(Text, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)  # milliseconds
    frame_count = Column(Integer, nullable=True)
    active = Column(Boolean, unique=False, default=True)
    private = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Video: {self.name} | {self.url}>"


class Liquid(Base):

    __tablename__ = "liquid"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    video_id = Column(Integer, ForeignKey("video.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    url = Column(String, nullable=True)
    treatment_id = Column(Integer, ForeignKey("treatment.id"))
    active = Column(Boolean, unique=False, default=True)
    private = Column(Boolean, default=False)
    job_id = Column(String, nullable=True)
    processing = Column(Boolean, default=False)
    treatment = relationship("Treatment", backref="liquids")
    video = relationship("Video", backref="liquids")

    def __repr__(self):
        return f"<Liquid: {self.id}>"


class Treatment(Base):

    __tablename__ = "treatment"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    controller_id = Column(Integer, ForeignKey("controller.id"))
    name = Column(String(200), nullable=False)
    desc = Column(Text, nullable=True)
    controller = relationship("Controller", backref="treatments")

    def __repr__(self):
        return f"<Treatment: {self.id} | {self.name}>"


class Controller(Base):

    __tablename__ = "controller"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __repr__(self):
        return f"<Controller: {self.name}>"
