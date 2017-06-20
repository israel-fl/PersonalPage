from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, abort, current_app as app
from flask_mail import Mail, Message
from flask_login import logout_user, login_user, current_user, login_required
from app.models.user import User, VerifyEmailRequest, RemoteSourceUser
from database.db_adapter import db
from app.http.middleware.decorators import validate_request
from werkzeug.security import generate_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import hashlib
from app.http.middleware.generators import generate_hash

blueprint = Blueprint('register', __name__)


@blueprint.route('/', methods=["GET", "POST"])
def register():


    def post():
        try:
            password = generate_password_hash(request.form.get('password'))
            email = request.form.get("email")
            name = request.form.get("name")
            # Check if an account with the given credentials already exists
            if (User.query.filter(User.email == email).first()):
                flash('Sorry, that email is already in use', "danger")
            else:
                next = create_user(name, email,
                                   profile_image_url=None, password=password)
                return redirect(next)
        except Exception as e:
            print(e)
            db.rollback()
            flash("There was an error processing your request", "danger")
        return render_template("register/register.html")

    if request.method == 'POST':
        # redirect to the url post returns
        return post()
    # else the request is GET
    else:
        return render_template("register/register.html")


@blueprint.route('/verify', methods=["GET", "POST"])
@login_required
def verify_user():

    def post():
        from app.http.controllers.mail_senders import send_verify_email
        send_verify_email()
        return render_template("register/email_resent.html")

    if request.method == 'POST':
        return post()
    else:
        return render_template("register/verify.html")


@blueprint.route('/activate', methods=["GET"])
def activate_user():
    try:
        token = request.args.get("token")
        # check if the token matches the database
        verify_obj = VerifyEmailRequest.query.filter(VerifyEmailRequest.token == hashlib.sha256(token).hexdigest()).first()
        if (verify_obj is not None):
            # get the related user
            user = User.query.filter(User.id == verify_obj.user_id).first()
            if (user.verified):
                abort(404)
            user.verified = True
            verify_obj.completed = True
            db.commit()
            return render_template("register/successfully_verified.html")
        # else the user is not authorized
        else:
            db.rollback()
            abort(404)
    except Exception:
        abort(404)


@blueprint.route("/terms", methods=["GET"])
def show_terms():
    return render_template("policies/terms.html")


@blueprint.route("/policy", methods=["GET"])
def show_policy():
    return render_template("policies/policy.html")


@blueprint.route('/social', methods=["GET", "POST"])
def register_social_account():


    def post():
        google_id = request.form.get("google-id")
        facebook_id = request.form.get("fb-id")
        email = request.form.get("social-email")
        name = request.form.get("social-name")
        image_url = request.form.get("social-image")
        if email is None:
            return render_template("register/register_email_only.html",
                                   google_id=google_id,
                                   facebook_id=facebook_id,
                                   name=name,
                                   image_url=image_url)
        else:
            # check if the email is already taken
            user = User.query.filter(User.email == email).first()
            # if it does log them in
            if user:
                # check if this user has used a social login before,
                # try to merge accounts
                # check which id was supplied
                if user.remote_user.google_id == google_id:
                    return check_current_user_level()
                elif user.remote_user.fb_id == facebook_id:
                    return check_current_user_level()
                elif google_id:
                    user.remote_user.google_id = google_id
                    db.commit()
                else:
                    user.remote_user.fb_id = facebook_id
                    db.commit()
                # if the user has not verified their account redirect
                # them to the verification portal
                return redirect(url_for("register.verify_user"))
            # user is logged in with this function
            next = create_user(name, email, image_url)
            print(next)
            print("Next finished")
            create_remote_user(google_id, facebook_id)
            return redirect(next)

    if request.method == 'POST':
        return post()


def check_current_user_level():
    if (current_user.is_active):
        if current_user.access_level >= 2:
            return redirect(url_for("dashboard.dashboard"))
        else:
            return redirect(url_for("home.account"))


def create_remote_user(google_id, facebook_id):
    # hence current_user can be accessed afterwards
    if google_id:
        remote_user = RemoteSourceUser(user_id=current_user.id,
                                       google_id=google_id)
    else:
        remote_user = RemoteSourceUser(user_id=current_user.id,
                                       fb_id=facebook_id)
    try:
        db.add(remote_user)
        db.commit()
    except Exception:
        db.rollback()


@blueprint.route('/social/email', methods=["GET", "POST"])
def missing_email():

    def post():
        name = request.form.get("name")
        email = request.form.get("email")
        image_url = request.form.get("social-image")
        google_id = request.form.get("google-id")
        facebook_id = request.form.get("fb-id")
        # user is logged in with this function
        next = create_user(name, email, image_url)
        # hence current_user can be accessed afterwards
        if google_id:
            remote_user = RemoteSourceUser(user_id=current_user.id,
                                           google_id=google_id)
        else:
            remote_user = RemoteSourceUser(user_id=current_user.id,
                                           fb_id=facebook_id)
        try:
            db.add(remote_user)
            db.commit()
        except Exception:
            db.rollback()
        return redirect(next)

    if request.method == 'POST':
        return post()


def create_user(name, email, profile_image_url=None, password=""):

    if profile_image_url is None:
        profile_image_url = url_for('static', filename='images/default_logo.png')
    user = User(name=name,
                email=email,
                password=password,
                profile_image_url=profile_image_url)
    # save the new user
    db.add(user)
    db.commit()

    # check if there is a user logged in, if so log them out
    if (current_user):
        logout_user()
    # login the current user so that we have a handle on the object
    login_user(user)
    print("Attempting to send email")
    from app.http.controllers.mail_senders import send_verify_email
    send_verify_email(user)
    print("returning")
    return url_for("register.verify_user")
