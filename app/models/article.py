from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey,\
    DateTime, Boolean, select, func
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime


class Article(Base):

    __tablename__ = "articles"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    author = Column('author', String, nullable=False)
    subtitle = Column("subtitle", String, nullable=False)
    content = Column("content", UnicodeText, nullable=False)
    slug = Column("slug", String, nullable=False)
    created = Column("created", DateTime, nullable=False, default=datetime.datetime.now())
    image_url = Column("image_url", String, nullable=True)
    image_alt = Column("image_alt", String, nullable=True)
    published = Column("published", Boolean, nullable=False, default=False)
