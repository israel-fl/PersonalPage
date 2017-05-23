from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey,\
    DateTime, Boolean, select, func
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime


class Post(Base):

    __tablename__ = "post"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    content = Column("text", UnicodeText, nullable=False)
    post_date = Column("created", DateTime, nullable=False, default=datetime.datetime.now())
    draft = Column("draft", Boolean, nullable=False, default=False)
    subtitle = Column("subtitle", String, nullable=False)
    slug = Column("slug", String, nullable=False)
    featured_image_url = Column("featured_image_url", String, nullable=True)
    published = Column("published", Boolean, nullable=False, default=False)


class Tag(Base):

    __tablename__ = "tag"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    text = Column("text", String, nullable=False)


class UserPost(Base):

    __tablename__ = "user_posts"
    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    post_id = Column("post_id", Integer, nullable=False)


class TagPost(Base):

    __tablename__ = "tag_posts"
    tag_id = Column("tag_id", Integer, primary_key=True, autoincrement=True)
    post_id = Column("post_id", Integer, nullable=False)
