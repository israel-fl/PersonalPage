from flask import Blueprint, request, jsonify, current_app as app, render_template
from .decorators import validate_access, validate_request
from werkzeug.security import generate_password_hash
from .database import db
import json
from .generators import generate_hash
from datetime import timedelta, datetime
import hashlib
from flask_mail import Mail, Message

blueprint = Blueprint('users', __name__)


register_schema = dict(name=dict(type='string', required=True),
                       username=dict(type='string', required=True),
                       email=dict(type='string', required=True),
                       phone=dict(type='string', required=True),
                       password=dict(type='string', required=True))


@blueprint.route('/', methods=["GET", "POST"])
def users():
    @validate_access(2)
    def get():
        users = list(db.users.find())
        return jsonify(users)

    @validate_request(register_schema)
    def post(data):
        try:
            data['password'] = generate_password_hash(data['password'])
            data["verified"] = False
            # check if username in use
            if (db.users.find_one({"username": data["username"]})):
                return json.dumps({"success": "false", "error": "username_exists"}, 403, {'ContentType': 'application/json'})
            elif (db.users.find_one({"email": data["email"]})):
                return json.dumps({"success": "false", "error": "email_exists"}, 403, {'ContentType': 'application/json'})
            db.users.insert_one(data)

            # Create a new request to verify email
            email_token = generate_hash()  # email THIS to the user
            hashed_id = hashlib.sha256(email_token).hexdigest()
            verify_obj = {"user": data["username"], "token": hashed_id, "created": datetime.now(), "completed": False}
            db.verify_email_requests.insert_one(verify_obj)
            return json.dumps({"success": "true"}, 201, {'ContentType': 'application/json'})
        except Exception as e:
            print(e)
            return json.dumps({"success": "false"}, 404, {'ContentType': 'application/json'})

    if request.method == 'GET':
        return get()
    else:
        return post()


verify_email_schema = dict(id=dict(type='string', required=True),
                           token=dict(type='string', required=True))


@blueprint.route('/<username>/verify', methods=["PUT"])
@validate_request(verify_email_schema)
def verify_user(data, username): # not sure about order of parameters
    try:
        # check if the user exists, if it does get the latest one
        verify_obj = db.verify_email_requests.find({"user": username}).limit(1).sort({"created":-1})
        if (verify_obj):
            # check if the token matches the database
            if (hashlib.sha256(data["token"]).hexdigest() == verify_obj["token"]):
                verify_obj["completed"] = True
                db.verify_email_requests.save(verify_obj)
                db.users.update_one({"id": id},
                    {
                    "$set": {
                        "verified": True
                        }
                    })
            return json.dumps({"success": "true"}, 200, {'ContentType': 'application/json'})
    except Exception as e:
        print(e)
        return json.dumps({"success": "false"}, 404, {'ContentType': 'application/json'})


# Verify user account [WIP]
def send_verify_email(user, email, url):

    mail = Mail(app)
    email = Message(
            subject="Please confirm your Delivery Sky account",
            sender="no-reply@deliverysky.com",
            recipients=[email])
    email.html = render_template("verify_account_email.html",
                                 name=user.display_username,
                                 url=url)

    mail.send(email)


# Reset Password [WIP]
def send_recovery_email(user, email, url):

    mail = Mail(app)
    email = Message(
            subject="IsraelFl Reset your Password",
            sender="no-reply@israelfl.com",
            recipients=[email])
    email.html = render_template("emails/verify_account_email.html",
                                 name=user.display_username,
                                 url=url)

    mail.send(email)


@blueprint.route('/<id>', methods=["GET", "PUT", "DELETE"])
def user(id):
    pass
