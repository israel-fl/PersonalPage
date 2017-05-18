from sqlalchemy import Column, Integer, String, ForeignKey,\
    DateTime, Boolean, select, func
from database.db_adapter import Base
from sqlalchemy.orm import relationship
import datetime


class User(Base):

    __tablename__ = "users"
    __id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    display_name = Column('display_name', String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    access_level = Column("level", Integer, nullable=False, default=0)
    verified = Column("verified", String, nullable=False, default="false")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__id).decode("utf-8")


class PasswordResetRequests(Base):

    __tablename__ = "password_reset_requests"
    email = Column("email", String, nullable=False, primary_key=True)
    token = Column("token", String, nullable=False)
    created = Column("created", String, nullable=False, default=datetime.datetime.now())


class VerifyEmailRequests(Base):

    __tablename__ = "verify_email_requests"
    email = Column("user_id", Integer, nullable=False)
    token = Column("token", String, nullable=False, primary_key=True)
    created = Column("created", String, nullable=False, default=datetime.datetime.now())
