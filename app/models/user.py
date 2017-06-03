from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime
from werkzeug.security import generate_password_hash


class User(Base):

    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    display_name = Column('display_name', String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    # New users are level 1 by default
    access_level = Column("level", Integer, nullable=False, default=1)
    verified = Column("verified", Boolean, nullable=False, default=False)
    created = Column("created", DateTime, nullable=False,
                     default=datetime.datetime.now())
    modified = Column("modified", DateTime, nullable=True)
    profile_image_url = Column("profile_image_url", String, nullable=True)
    description = Column("description", String, nullable=True)
    comments = relationship("Comment")

    def __init__(self, name, display_name, email, password,
                 access_level="1", verified=False):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = generate_password_hash(password)
        self.access_level = access_level
        self.verified = verified
        self.created = str(datetime.datetime.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        if (self.verified):
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        # transform id to unicode
        return str(self.id).decode("utf-8")


class PasswordResetRequest(Base):

    __tablename__ = "password_reset_requests"
    user_id = Column("user_id", String, nullable=False, primary_key=True)
    token = Column("token", String, nullable=False)
    created = Column("created", DateTime, nullable=False,
                     default=datetime.datetime.now())


class VerifyEmailRequest(Base):

    __tablename__ = "verify_email_requests"
    user_id = Column("user_id", Integer, nullable=False)
    token = Column("token", String, nullable=False, primary_key=True)
    created = Column("created", DateTime, nullable=False,
                     default=datetime.datetime.now())
    completed = Column("completed", Boolean, nullable=False, default=False)
