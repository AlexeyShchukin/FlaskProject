from typing import List, Optional

from sqlalchemy import Float, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = 'role'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

    users: Mapped[List['User']] = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['role.id'], name='user_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('role_id', 'role_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(75))
    password: Mapped[str] = mapped_column(String(255))
    repeat_password: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(30))
    phone: Mapped[Optional[str]] = mapped_column(String(45))
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    rating: Mapped[Optional[float]] = mapped_column(Float, server_default=text("'0'"))
    deleted: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    role: Mapped[Optional['Role']] = relationship('Role', back_populates='users')
    news: Mapped[List['News']] = relationship('News', back_populates='author')
    comments: Mapped[List['Comment']] = relationship('Comment', back_populates='author')


class News(Base):
    __tablename__ = 'news'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['user.id'], name='news_ibfk_1'),
        Index('author_id', 'author_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[Optional[int]] = mapped_column(Integer)
    moderated: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    author: Mapped[Optional['User']] = relationship('User', back_populates='news')
    comments: Mapped[List['Comment']] = relationship('Comment', back_populates='news')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['user.id'], name='comment_ibfk_1'),
        ForeignKeyConstraint(['news_id'], ['news.id'], name='comment_ibfk_2'),
        Index('author_id', 'author_id'),
        Index('news_id', 'news_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[Optional[int]] = mapped_column(Integer)
    news_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    author: Mapped[Optional['User']] = relationship('User', back_populates='comments')
    news: Mapped[Optional['News']] = relationship('News', back_populates='comments')
