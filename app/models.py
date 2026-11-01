from datetime import datetime, timezone
from typing import Optional, List
import uuid

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('photo_posts.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str] = mapped_column(String(8), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    avatar_file: Mapped[str] = mapped_column(String(256), default='default.jpg')
    avatar_config: Mapped[str] = mapped_column(String(512), default='{"body":"#2196F3","arms":"#4CAF50","legs":"#FFC107"}')
    language: Mapped[str] = mapped_column(String(2), default='tr')
    reset_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    reset_expiration: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    posts: Mapped[List["PhotoPost"]] = relationship(back_populates='author', cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates='author', cascade="all, delete-orphan")

    notifications_received: Mapped[List["Notification"]] = relationship(
        foreign_keys='Notification.recipient_id',
        back_populates='recipient',
        cascade="all, delete-orphan",
        lazy='dynamic'
    )
    notifications_sent: Mapped[List["Notification"]] = relationship(
        foreign_keys='Notification.sender_id',
        back_populates='sender',
        cascade="all, delete-orphan",
        lazy='dynamic'
    )

    messages_sent: Mapped[List["Message"]] = relationship(
        foreign_keys='Message.sender_id',
        back_populates='sender',
        cascade="all, delete-orphan",
        lazy='dynamic'
    )
    messages_received: Mapped[List["Message"]] = relationship(
        foreign_keys='Message.recipient_id',
        back_populates='recipient',
        cascade="all, delete-orphan",
        lazy='dynamic'
    )

    followed: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    liked_posts: Mapped[List["PhotoPost"]] = relationship(
        secondary=likes,
        backref=db.backref('likers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def unread_message_count(self):
        return self.messages_received.filter_by(is_read=False).count()

    def like_post(self, post):
        if not self.has_liked_post(post):
            self.liked_posts.append(post)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            self.liked_posts.remove(post)

    def has_liked_post(self, post):
        return self.liked_posts.filter(likes.c.post_id == post.id).count() > 0


class PhotoPost(db.Model):
    __tablename__ = 'photo_posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_file: Mapped[str] = mapped_column(String(256), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    author: Mapped["User"] = relationship(back_populates='posts')
    comments: Mapped[List["Comment"]] = relationship(back_populates='post', cascade="all, delete-orphan")

    camera_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    lens_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    iso: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    aperture: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    shutter_speed: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    editing_software: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)


class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    photo_post_id: Mapped[int] = mapped_column(ForeignKey('photo_posts.id'), nullable=False)

    author: Mapped["User"] = relationship(back_populates='comments')
    post: Mapped["PhotoPost"] = relationship(back_populates='comments')


class Notification(db.Model):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True)
    recipient_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False) # 'like', 'follow', 'comment'
    post_id: Mapped[Optional[int]] = mapped_column(ForeignKey('photo_posts.id'), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_read: Mapped[bool] = mapped_column(db.Boolean, default=False)

    recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id], back_populates='notifications_received')
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id], back_populates='notifications_sent')
    post: Mapped[Optional["PhotoPost"]] = relationship()

class Message(db.Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_read: Mapped[bool] = mapped_column(db.Boolean, default=False)

    sender: Mapped["User"] = relationship(foreign_keys=[sender_id], back_populates='messages_sent')
    recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id], back_populates='messages_received')


class Game(db.Model):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_code: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    player1_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    player2_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    
    player1_score: Mapped[int] = mapped_column(Integer, default=0)
    player2_score: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status: 'waiting', 'in_progress', 'completed', 'cancelled'
    status: Mapped[str] = mapped_column(String(32), default='waiting')
    winner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    
    current_round_num: Mapped[int] = mapped_column(Integer, default=1)
    target_score: Mapped[int] = mapped_column(Integer, default=3)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    player1: Mapped["User"] = relationship(foreign_keys=[player1_id])
    player2: Mapped[Optional["User"]] = relationship(foreign_keys=[player2_id])
    winner: Mapped[Optional["User"]] = relationship(foreign_keys=[winner_id])
    rounds: Mapped[List["GameRound"]] = relationship(back_populates='game', cascade="all, delete-orphan", order_by="GameRound.round_num")


class GameRound(db.Model):
    __tablename__ = 'game_rounds'

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'), nullable=False)
    round_num: Mapped[int] = mapped_column(Integer, nullable=False)
    theme: Mapped[str] = mapped_column(String(128), nullable=False)
    theme_description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    
    # Photo image filenames or Cloudinary URLs
    player1_image: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    player2_image: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    
    player1_uploaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    player2_uploaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # AI judging results
    winner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    is_tie: Mapped[bool] = mapped_column(db.Boolean, default=False)
    ai_reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_feedback_p1: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_feedback_p2: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Round status: 'uploading', 'judging', 'completed'
    status: Mapped[str] = mapped_column(String(32), default='uploading')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    game: Mapped["Game"] = relationship(back_populates='rounds')
    winner: Mapped[Optional["User"]] = relationship(foreign_keys=[winner_id])

