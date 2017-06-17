from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, abort, current_app as app
from flask_mail import Mail, Message
from flask_login import logout_user, login_user, current_user, login_required
from app.models.user import User, VerifyEmailRequest
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
                return create_user(name, email, password)
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
        data = request.get_json()
        user_id = data.get("user_id")
        email = data.get("email")
        name = data.get("name")
        image_url = data.get("image_url")
        if email is None:
            render_template("register/register.html",
                            user_id=user_id,
                            name=name,
                            image_url=image_url)
        elif image_url is None:
            return create_user(name, email, image_url)
        else:
            return create_user(name, email)

    if request.method == 'POST':
        return post()


def create_user(name, email, password="",
    profile_image_url=url_for('static', filename='images/default_logo.png')):

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
    from app.http.controllers.mail_senders import send_verify_email
    send_verify_email(user)
    return redirect(url_for("register.verify_user"))

# # Enable message flashing for errors in form validation
# def flash_errors(form):
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"Error in the %s field - %s" % (
#                 getattr(form, field).label.text,
#                 error
#             ), "danger")
