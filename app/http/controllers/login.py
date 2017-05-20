from flask import render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user, login_user
from app.models.users import User, PasswordResetRequest
from database.db_adapter import db
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from app.http.middleware.generators import generate_hash
import hashlib

blueprint = Blueprint('login', __name__)


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])


@blueprint.route("/", methods=["GET", "POST"])
def login():


    def post():
        form = LoginForm(request.form)
        if (form.validate()):
            email = request.form.get("email")
            password = request.form.get("password")
            user = db.query(User).filter(User.email == email).first()
            # user found
            if (user):
                password_match = check_password_hash(user.password, password)
                # password matches
                if (password_match):
                    login_user(user)
                    return redirect(url_for("dashboard.dashboard"))
                else:
                    flash("Sorry, email or password incorrect", "danger")
            else:
                flash("Sorry we could not find an account associated with that email", "info")
        # if this was reached, there were errors
        return render_template("login/login.html")

    # Determine the request type
    if (request.method == "POST"):
        return post()
    else:
        return render_template("login/login.html")


@blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    def post():
        email = request.form.get("email")
        user = db.query(User).filter(User.email == email).first()
        if (user):
            try:
                # Create a new request to verify email
                email_token = generate_hash()  # email THIS to the user
                hashed_id = hashlib.sha256(email_token).hexdigest()
                password_reset_request = PasswordResetRequest(user_id=user.id,
                                                               token=hashed_id)
                db.add(password_reset_request)
                db.commit()
                from app.http.controllers.mail_senders import send_recovery_email
                send_recovery_email(user.display_name, user.email, email_token)
                return render_template("login/reset_password.html")
            except Exception:
                flash("There was an error processing your request", "danger")
                return render_template("login/begin_reset.html")
    # Determine the request type
    if (request.method == "POST"):
        return post()
    else:
        return render_template("login/begin_reset.html")
