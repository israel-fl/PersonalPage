from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, abort, current_app as app
from flask_mail import Mail, Message
from flask_login import logout_user, login_user, current_user, login_required
from app.models.users import User, VerifyEmailRequest
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
            username = request.form.get("username")
            # Check if an account with the given credentials already exists
            if (db.query(User).filter(User.email == email).first()):
                flash('Sorry, there is already an account associated with that email', "danger")
            elif (db.query(User).filter(User.display_name == username).first()):
                flash('Sorry, that username has already been taken', "danger")
            else:
                user = User(name=name,
                            display_name=username,
                            email=email,
                            password=password)
                # save the new user
                db.add(user)
                db.commit()

                # check if there is a user logged in, if so log them out
                if (current_user):
                    logout_user()
                # login the current user so that we have a handle on the object
                login_user(user)
                from app.http.controllers.mail_senders import send_verify_email
                send_verify_email()
                return redirect(url_for("register.verify_user"))
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
        verify_obj = db.query(VerifyEmailRequest).filter(VerifyEmailRequest.token == hashlib.sha256(token).hexdigest()).first()
        if (verify_obj is not None):
            # get the related user
            user = db.query(User).filter(User.id == verify_obj.user_id).first()
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


# # Enable message flashing for errors in form validation
# def flash_errors(form):
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"Error in the %s field - %s" % (
#                 getattr(form, field).label.text,
#                 error
#             ), "danger")
