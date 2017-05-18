from sqlalchemy import Column, Integer, String, LONGTEXT, ForeignKey,\
    DateTime, Boolean, select, func
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime


class Entry(Base):

    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    author = Column('author', String, nullable=False)
    subtitle = Column("subtitle", String, nullable=False)
    image = Column("image", String, nullable=False)
    content = Column("content", LONGTEXT, nullable=False)
    slug = Column("slug", String, nullable=False)
    created = Column("created", String, nullable=False, default=datetime.datetime.now())
