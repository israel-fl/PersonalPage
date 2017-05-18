from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user
from app.models.users import User
from database.db_adapter import db


blueprint = Blueprint('login', __name__)


@blueprint.route("/", methods=["GET", "POST"])
def login():


    def post():
        pass

    # Determine the request type
    if (request.method == "POST"):
        post()

    return render_template("login/login.html")


# Reset password endpoint
def send_recovery_email(username, email_addr, token):
    mail = Mail(app)
    email = Message(
            subject="Reset your password at Israel FL",
            sender="no-reply@israelfl.com",
            recipients=[email_addr])
    email.html = render_template("emails/reset_password_email.html",
                                 usename=username,
                                 token=token)

    mail.send(email)
