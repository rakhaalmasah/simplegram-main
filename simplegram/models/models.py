from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from config import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200))
    fullname: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    profpic: Mapped[str] = mapped_column(String(200), nullable=True, default='anonymous.jpg')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    posts = relationship('Post')
    # Ini Tambahan Kode Saya
    bookmarks = relationship('Bookmark', back_populates='user')
    likes = relationship('Like', back_populates='user')

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    image: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    # Ini tambahan kode saya
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    bookmarks = relationship('Bookmark', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    #Ini tambahan kode saya
    post = relationship('Post')

# In tambahan kode saya
class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    user = relationship('User', back_populates='bookmarks')
    post = relationship('Post', back_populates='bookmarks')

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    sender = relationship('User', foreign_keys=[sender_id])
    receiver = relationship('User', foreign_keys=[receiver_id])

class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    post_id = db.Column(db.Integer, ForeignKey('post.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')