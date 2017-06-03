from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey,\
    DateTime, Boolean
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime


class Post(Base):

    __tablename__ = "posts"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column("title", String, nullable=False)
    subtitle = Column("subtitle", String, nullable=False)
    content = Column("content", UnicodeText, nullable=False)
    featured_image_url = Column("featured_image_url", String, nullable=True)
    slug = Column("slug", String, nullable=False)
    tags = Column("tags", String, nullable=True)
    published = Column("published", Boolean, nullable=False, default=False)
    created = Column("created", DateTime, nullable=False, default=datetime.datetime.now())
    modified = Column("modified", DateTime, nullable=True, default=datetime.datetime.now())
    comments = relationship("Comment")
    author = relationship("User", back_populates="articles")

class Comment(Base):

    __tablename__ = "post_comments"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    title = Column("title", String, nullable=False)
    comment = Column("comment", UnicodeText, nullable=False)
    created = Column("created", DateTime, nullable=False, default=datetime.datetime.now())
    modified = Column("modified", DateTime, nullable=True, default=datetime.datetime.now())
