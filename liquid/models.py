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
from .database import Base


class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String, nullable=False)
    poster = Column(String, nullable=True)
    active = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return f"<Video: {self.name} | {self.url}>"


class Liquid(Base):
    __tablename__ = "liquid"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    video_id = Column(Integer, ForeignKey("video.id"))
    liquid = Column(JSON, nullable=False)
    method_id = Column(Integer, ForeignKey("liquid_method.id"))
    desc = Column(Text)
    active = Column(Boolean, unique=False, default=True)
    method = relationship("LiquidMethod", backref="liquids")
    video = relationship("Video", backref="liquids")

    def __repr__(self):
        return f"<Liquid: {self.id}>"


class LiquidMethod(Base):
    __tablename__ = "liquid_method"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f"<Liquid Method: {self.name}>"
