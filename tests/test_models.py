from app.models.user import User, PasswordResetRequest,\
    VerifyEmailRequest, RemoteSourceUser
from app.models.blog import Post, Comment
from app.models.pagination import Pagination
from werkzeug.security import generate_password_hash
from database.db_adapter import db
from flask import url_for


def test_user_model(session):
    password = generate_password_hash("test_password")
    user = User(name="Test",
                email="test@email.com",
                password=password,
                profile_image_url = "http://www.georgiaaquarium.org/images/default-source/content-boxes/1x1/penguinplush1x1.jpg?sfvrsn=1",
                access_level=1,
                verified=True)
    db.add(user)
    db.commit()
    assert user.id > 0


def test_password_reset(session):
    # first add a user to have a reference to it
    password = generate_password_hash("test_password")
    user = User(name="Test",
                email="test2@email.com",
                password=password,
                profile_image_url = "http://www.georgiaaquarium.org/images/default-source/content-boxes/1x1/penguinplush1x1.jpg?sfvrsn=1",
                access_level=1,
                verified=True)
    db.add(user)
    db.commit()

    reset = PasswordResetRequest(user_id=user.id, token="RandomAlphanumericString")
    db.add(reset)
    db.commit()
    assert reset.user_id > 0


def test_email_verification(session):
    # first add a user to have a reference to it
    password = generate_password_hash("test_password")
    user = User(name="Test",
                email="test3@email.com",
                password=password,
                profile_image_url = "http://www.georgiaaquarium.org/images/default-source/content-boxes/1x1/penguinplush1x1.jpg?sfvrsn=1",
                access_level=1,
                verified=True)
    db.add(user)
    db.commit()

    verify = VerifyEmailRequest(user_id=user.id, token="RandomAlphanumericString",
                               completed=True)
    db.add(verify)
    db.commit()
    assert verify.user_id > 0

