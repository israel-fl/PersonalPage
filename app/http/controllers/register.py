from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user
from app.models.users import User, VerifyEmailRequest
from database.db_adapter import db
from app.http.middleware.decorators import validate_request
from werkzeug.security import generate_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators


blueprint = Blueprint('register', __name__)


class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=40)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])


@blueprint.route('/', methods=["GET", "POST"])
def users():


    def post(data):
        try:
            form = RegistrationForm(request.form)
            if (form.validate()):
                data['password'] = generate_password_hash(data['password'])
                data["verified"] = False
                email = data.get("email")
                # Check if an account with the given credentials already exists
                if (db.query(User).filter(User.email == email).first() is not None):
                    flash('Sorry, there is already an account associated with that email')
                elif (db.query(User).filter(User.email == email).first() is not None):
                    flash('Sorry, that username has already been taken')
                else:
                    user = new User(name=data.get("name"),
                                    display_name=data.get("username"),
                                    email=email,
                                    password=data.get("pass"))
                    # save the new user
                    db.commit()

                    # Create a new request to verify email
                    email_token = generate_hash()  # email THIS to the user
                    hashed_id = hashlib.sha256(email_token).hexdigest()
                    verify_email = new VerifyEmailRequest(email=email,
                                                          token=hashed_id)
                    send_verify_email(email)
                    db.commit()
                    return render_template("register/verify.html")
        except Exception as e:
            print(e)
            db.rollback()
            return json.dumps({"success": "false"}, 404, {'ContentType': 'application/json'})

    if request.method == 'POST':
        post()

    return render_template("register/register.html")


@blueprint.route('/verify', methods=["post"])
@validate_request(verify_email_schema)
def verify_user(data, username): # not sure about order of parameters
    try:
        # check if the token matches the database
        verify_obj = db.query.find(VerifyEmailRequest.token == hashlib.sha256(token).hexdigest()).first()
        if (verify_obj is not None):
            # get the related user
            user = db.query.find(User.id == verify_obj.user_id).first()
            user.verfied = "true"
            return render_template("register/successfully_verified.html")
        # else the user is not authorized
        else:
            return render_template("unauth.html")
    except Exception as e:
        return render_template("unauth.html")


# Verify user account
def send_verify_email(username, email_addr, token):
    mail = Mail(app)
    email = Message(
            subject="Verify your email with Israel FL",
            sender="no-reply@israelfl.com",
            recipients=[email_addr])
    email.html = render_template("emails/verify_email.html",
                                 usename=username,
                                 token=token)

    mail.send(email)


@blueprint.route("/terms", methods=["GET"])
def show_terms():
    return render_template("policies/terms.html")


@blueprint.route("/policy", methods=["GET"])
def show_policy():
    return render_template("policies/policy.html")
