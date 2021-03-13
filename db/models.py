from sqlalchemy import Column, Integer, String, func, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(duration >= 0, name='check_duration_positive'), {}
    )


class Podcast(Base):
    __tablename__ = "podcast"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    host = Column(String(100), index=True, nullable=False)
    participants = Column(ARRAY(String(100)), nullable=True)

    __table_args__ = (
        CheckConstraint(duration >= 0, name='check_duration_positive'), {}
    )


class Audiobook(Base):
    __tablename__ = "audiobook"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    author = Column(String(100), index=True, nullable=False)
    narrator = Column(String(100), index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(duration >= 0, name='check_duration_positive'), {}
    )
