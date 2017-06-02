from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey,\
    DateTime, Boolean, select, func
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime


class Post(Base):

    __tablename__ = "posts"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    author = Column("author", String, nullable=False)
    title = Column("title", String, nullable=False)
    subtitle = Column("subtitle", String, nullable=False)
    content = Column("content", UnicodeText, nullable=False)
    featured_image_url = Column("featured_image_url", String, nullable=True)
    slug = Column("slug", String, nullable=False)
    tags = Column("tags", String, nullable=True)
    published = Column("published", Boolean, nullable=False, default=False)
    created = Column("created", DateTime, nullable=False, default=datetime.datetime.now())
    modified = Column("modified", DateTime, nullable=True, default=datetime.datetime.now())
