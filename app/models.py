from datetime import datetime, timezone
from typing import Optional, List

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
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    avatar_file: Mapped[str] = mapped_column(String(256), default='default.jpg')

    posts: Mapped[List["PhotoPost"]] = relationship(back_populates='author', cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates='author', cascade="all, delete-orphan")

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
