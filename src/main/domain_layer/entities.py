from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, Date, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class GenderPreference(Enum):
    MALE = 'male'
    FEMALE = 'female'
    BOTH = 'both'
    OTHER = 'other'

class User(Base):
    __tablename__ = 'users'
    Id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    passwordHash = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    createdAt = Column(Date, default=datetime.now())
    updatedAt = Column(Date, default=datetime.now(), onupdate=datetime.now())

    profile = relationship("Profile", uselist=False, back_populates="user")
    swipes = relationship("Swipe", foreign_keys="Swipe.swiperId", back_populates="swiper")
    matches = relationship("Match", foreign_keys="Match.user1Id", back_populates="user1")
    notifications = relationship("Notification", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    reports = relationship("Report", foreign_keys="Report.reporterId", back_populates="reporter")
    blocks = relationship("Block", foreign_keys="Block.blockerId", back_populates="blocker")

class Profile(Base):
    __tablename__ = 'profiles'
    Id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.Id'), unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    bio = Column(String)
    gender = Column(SQLEnum(Gender))
    birthdate = Column(Date)
    location = Column(String)
    createdAt = Column(Date, default=datetime.now())
    updatedAt = Column(Date, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="profile")
    photos = relationship("Photo", back_populates="profile")
    preference = relationship("Preference", uselist=False, back_populates="profile")

class Photo(Base):
    __tablename__ = 'photos'
    Id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profiles.Id'), nullable=False)
    url = Column(String, nullable=False)
    order = Column(Integer)
    createdAt = Column(Date, default=datetime.now())

    profile = relationship("Profile", back_populates="photos")

class Preference(Base):
    __tablename__ = 'preferences'
    Id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profiles.Id'), unique=True, nullable=False)
    minAge = Column(Integer)
    maxAge = Column(Integer)
    maxDistance = Column(Integer)
    gender_preference = Column(SQLEnum(GenderPreference))
    createdAt = Column(Date, default=datetime.now())
    updatedAt = Column(Date, default=datetime.now(), onupdate=datetime.now())

    profile = relationship("Profile", back_populates="preference")

class Swipe(Base):
    __tablename__ = 'swipes'
    Id = Column(Integer, primary_key=True)
    swiperId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    swipedId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    action = Column(String, nullable=False)
    createdAt = Column(Date, default=datetime.now())

    swiper = relationship("User", foreign_keys=[swiperId], back_populates="swipes")
    swiped = relationship("User", foreign_keys=[swipedId])

class Match(Base):
    __tablename__ = 'matches'
    Id = Column(Integer, primary_key=True)
    user1Id = Column(Integer, ForeignKey('users.Id'), nullable=False)
    user2Id = Column(Integer, ForeignKey('users.Id'), nullable=False)
    createdAt = Column(Date, default=datetime.now())
    isActive = Column(Boolean, default=True)

    user1 = relationship("User", foreign_keys=[user1Id], back_populates="matches")
    user2 = relationship("User", foreign_keys=[user2Id])
    messages = relationship("Message", back_populates="match")

class Message(Base):
    __tablename__ = 'messages'
    Id = Column(Integer, primary_key=True)
    matchId = Column(Integer, ForeignKey('matches.Id'), nullable=False)
    senderId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    content = Column(String, nullable=False)
    createdAt = Column(Date, default=datetime.now())
    isRead = Column(Boolean, default=False)

    match = relationship("Match", back_populates="messages")
    sender = relationship("User")

class Notification(Base):
    __tablename__ = 'notifications'
    Id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)
    createdAt = Column(Date, default=datetime.now())
    isRead = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    Id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    plan = Column(String, nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    isActive = Column(Boolean, default=True)
    createdAt = Column(Date, default=datetime.now())
    updatedAt = Column(Date, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="subscriptions")

class Report(Base):
    __tablename__ = 'reports'
    Id = Column(Integer, primary_key=True)
    reporterId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    reportedId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    reason = Column(String, nullable=False)
    createdAt = Column(Date, default=datetime.now())

    reporter = relationship("User", foreign_keys=[reporterId], back_populates="reports")
    reported = relationship("User", foreign_keys=[reportedId])

class Block(Base):
    __tablename__ = 'blocks'
    Id = Column(Integer, primary_key=True)
    blockerId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    blockedId = Column(Integer, ForeignKey('users.Id'), nullable=False)
    createdAt = Column(Date, default=datetime.now())

    blocker = relationship("User", foreign_keys=[blockerId], back_populates="blocks")
    blocked = relationship("User", foreign_keys=[blockedId])