from flask import render_template, request, flash, redirect, url_for,\
 Blueprint
from flask_login import login_user, current_user
from app.models.user import User, PasswordResetRequest
from database.db_adapter import db
from werkzeug.security import check_password_hash
from app.http.middleware.generators import generate_hash
import hashlib

blueprint = Blueprint('login', __name__)


@blueprint.route("/", methods=["GET", "POST"])
def login():


    def post():
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter(User.email == email).first()
        print(user)
        # user found
        if (user):
            password_match = check_password_hash(user.password, password)
            print(password_match)
            # password matches
            if (password_match):
                login_user(user)
                if (current_user.is_active):
                    if current_user.access_level >= 2:
                        return redirect(url_for("dashboard.dashboard"))
                    else:
                        return redirect(url_for("home.account"))
                else:
                    # if the user has not verified their account redirect
                    # them to the verification portal
                    return redirect(url_for("register.verify_user"))
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
        # check if there is a user logged in, if so send him to the dashboard
        print(current_user.is_active())
        if (current_user.is_active()):
            return redirect(url_for("dashboard.dashboard"))
        return render_template("login/login.html")


@blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    def post():
        email = request.form.get("email")
        user = User.query.filter(User.email == email).first()
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
                send_recovery_email(user.name, user.email, email_token)
                return render_template("login/reset_password.html")
            except Exception:
                flash("There was an error processing your request", "danger")
                return render_template("login/begin_reset.html")
    # Determine the request type
    if (request.method == "POST"):
        return post()
    else:
        return render_template("login/begin_reset.html")
