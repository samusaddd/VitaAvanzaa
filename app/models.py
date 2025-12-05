
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    dvi_profiles = relationship("DVIProfile", back_populates="user")
    feed_posts = relationship("FeedPost", back_populates="user")

class DVIProfile(Base):
    __tablename__ = "dvi_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    overall_score = Column(Float)
    financial = Column(Float)
    career = Column(Float)
    wellbeing = Column(Float)
    integration = Column(Float)
    skills = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="dvi_profiles")

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    country = Column(String, nullable=True)
    score_match = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class FeedPost(Base):
    __tablename__ = "feed_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tag = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feed_posts")
