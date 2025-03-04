from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from .base import Base, BaseModel


class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    OTHER = "other"


class SwipeAction(Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    SUPERLIKE = "superlike"


class NotificationType(Enum):
    MATCH = "match"
    MESSAGE = "message"
    LIKE = "like"
    SYSTEM = "system"


class SubscriptionPlan(Enum):
    FREE = "free"
    PREMIUM = "premium"
    GOLD = "gold"


class User(Base, BaseModel):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sent_swipes = relationship("Swipe", foreign_keys="Swipe.swiper_id", back_populates="swiper")
    received_swipes = relationship("Swipe", foreign_keys="Swipe.swiped_id", back_populates="swiped")
    notifications = relationship("Notification", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_active={self.is_active})>"




class Profile(Base, BaseModel):
    __tablename__ = 'profiles'

    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    bio = Column(String(500))
    gender = Column(SQLAlchemyEnum(GenderType), nullable=False)
    birthdate = Column(DateTime, nullable=False)
    location = Column(String(255))

    # Relationships
    user = relationship("User", back_populates="profile")
    photos = relationship("Photo", back_populates="profile", cascade="all, delete-orphan")
    preference = relationship("Preference", back_populates="profile", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Profile(id={self.id}, username='{self.username}', user_id={self.user_id})>"


class Photo(Base, BaseModel):
    __tablename__ = 'photos'

    url = Column(String(255), nullable=False)
    order = Column(Integer, default=0)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)

    # Relationships
    profile = relationship("Profile", back_populates="photos")

    def __repr__(self):
        return f"<Photo(id={self.id}, profile_id={self.profile_id}, order={self.order})>"


class Swipe(Base, BaseModel):
    __tablename__ = 'swipes'

    action = Column(SQLAlchemyEnum(SwipeAction), nullable=False)
    swiper_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    swiped_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    swiper = relationship("User", foreign_keys=[swiper_id], back_populates="sent_swipes")
    swiped = relationship("User", foreign_keys=[swiped_id], back_populates="received_swipes")

    def __repr__(self):
        return f"<Swipe(id={self.id}, swiper_id={self.swiper_id}, swiped_id={self.swiped_id}, action={self.action})>"


class Match(Base, BaseModel):
    __tablename__ = 'matches'

    user1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    messages = relationship("Message", back_populates="match", cascade="all, delete-orphan")
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

    def __repr__(self):
        return f"<Match(id={self.id}, user1_id={self.user1_id}, user2_id={self.user2_id}, is_active={self.is_active})>"


class Message(Base, BaseModel):
    __tablename__ = 'messages'

    content = Column(String(1000), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    is_read = Column(Boolean, default=False)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    match = relationship("Match", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, match_id={self.match_id}, is_read={self.is_read})>"


class Notification(Base, BaseModel):
    __tablename__ = 'notifications'

    content = Column(String(255), nullable=False)
    type = Column(SQLAlchemyEnum(NotificationType), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_read = Column(Boolean, default=False)
    related_id = Column(Integer, nullable=True)  # Optional ID for related entity (match_id, message_id, etc.)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type}, is_read={self.is_read})>"


class Preference(Base, BaseModel):
    __tablename__ = 'preferences'

    profile_id = Column(Integer, ForeignKey('profiles.id'), unique=True, nullable=False)
    min_age = Column(Integer, default=18)
    max_age = Column(Integer, default=100)
    max_distance = Column(Integer, default=50)  # in kilometers
    gender_preference = Column(SQLAlchemyEnum(GenderType), nullable=True)  # NULL means all genders

    # Relationships
    profile = relationship("Profile", back_populates="preference")

    def __repr__(self):
        return f"<Preference(id={self.id}, profile_id={self.profile_id}, min_age={self.min_age}, max_age={self.max_age})>"


class Subscription(Base, BaseModel):
    __tablename__ = 'subscriptions'

    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    plan = Column(SQLAlchemyEnum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan={self.plan}, is_active={self.is_active})>"


class Report(Base, BaseModel):
    __tablename__ = 'reports'

    reason = Column(String(500), nullable=False)
    reporter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reported_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default="pending")  # pending, reviewed, closed

    # Relationships
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="sent_reports")
    reported = relationship("User", foreign_keys=[reported_id], back_populates="received_reports")

    def __repr__(self):
        return f"<Report(id={self.id}, reporter_id={self.reporter_id}, reported_id={self.reported_id})>"


class Block(Base, BaseModel):
    __tablename__ = 'blocks'

    blocker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blocked_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    blocker = relationship("User", foreign_keys=[blocker_id], back_populates="blocks_made")
    blocked = relationship("User", foreign_keys=[blocked_id], back_populates="blocks_received")

    def __repr__(self):
        return f"<Block(id={self.id}, blocker_id={self.blocker_id}, blocked_id={self.blocked_id})>"