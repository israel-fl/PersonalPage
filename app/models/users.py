from sqlalchemy import Column, Integer, String, ForeignKey,\
    DateTime, Boolean, select, func
from app import db
from sqlalchemy.orm import relationship
import datetime
from werkzeug.security import generate_password_hash


class User(db.Model):

    __tablename__ = "users"
    id = Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = Column("name", db.String, nullable=False)
    display_name = Column('display_name', db.String, nullable=False)
    email = Column("email", db.String, nullable=False)
    password = Column("password", db.String, nullable=False)
    # New users are level 1 by default
    access_level = Column("level", db.Integer, nullable=False, default=1)
    verified = Column("verified", db.Boolean, nullable=False, default=False)
    created = Column("created", db.DateTime, nullable=False,
                     default=datetime.datetime.now())
    modified = Column("modified", db.DateTime, nullable=True)

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


class PasswordResetRequest(db.Model):

    __tablename__ = "password_reset_requests"
    user_id = Column("user_id", db.String, nullable=False, primary_key=True)
    token = Column("token", db.String, nullable=False)
    created = Column("created", db.DateTime, nullable=False,
                     default=datetime.datetime.now())


class VerifyEmailRequest(db.Model):

    __tablename__ = "verify_email_requests"
    user_id = Column("user_id", db.Integer, nullable=False)
    token = Column("token", db.String, nullable=False, primary_key=True)
    created = Column("created", db.DateTime, nullable=False,
                     default=datetime.datetime.now())
    completed = Column("completed", db.Boolean, nullable=False, default=False)
