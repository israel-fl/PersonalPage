from app import mail
from flask_mail import Message
from flask_login import LoginManager, logout_user, login_user, current_user, login_required
import hashlib
from app.models.users import VerifyEmailRequest
from database.db_adapter import db
from flask import render_template
from app.http.middleware.generators import generate_hash


# Verify user account
def send_verify_email():
    # user must be logged in order to access this, so let's get the session
    user = current_user
    # Create a new request to verify email
    email_token = generate_hash()  # email THIS to the user
    hashed_id = hashlib.sha256(email_token).hexdigest()
    verify_email = VerifyEmailRequest(user_id=user.id,
                                      token=hashed_id)
    # Add the request to the database
    db.add(verify_email)
    db.commit()
    recipients = list()
    recipients.append(user.email)

    url = "https://www.israelfl.com/register/activate?token={}".format(email_token)
    email = Message(
            subject="Verify your email with Israel FL",
            sender="no-reply@israelfl.com",
            recipients=recipients)
    email.html = render_template("emails/verify_email.html",
                                 username=user.display_name,
                                 url=url)
    print(recipients)
    mail.send(email)
    print("email sent")


# Reset password endpoint
def send_recovery_email(username, email_addr, token):
    url = "https://www.israelfl.com/register/activate?token={}".format(token)
    print(url) ## for testing only
    recipients = list()
    recipients.append(email_addr)
    email = Message(
            subject="Verify your email with Israel FL",
            sender="no-reply@israelfl.com",
            recipients=recipients)
    email.html = render_template("emails/verify_email.html",
                                 usename=username,
                                 url=url)
    mail.send(email)


def send_message_email(name, email_addr, phone, message):
    email = Message(
            subject="A new message from {}!".format(name),
            sender="no-reply@israelfl.com",
            recipients=["iflore04@gmail.com"])
    email.html = render_template("emails/contact_email.html",
                                 name=name,
                                 email=email_addr,
                                 phone=phone,
                                 message=message)
    mail.send(email)
