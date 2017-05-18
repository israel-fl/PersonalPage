from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user
from app.models.users import User, VerifyEmailRequest
from database.db_adapter import db
from app.http.middleware.decorators import validate_request, validate_access
from werkzeug.security import generate_password_hash


blueprint = Blueprint('dashboard', __name__)


@blueprint.route("/", methods=["GET"])
@validate_access
def dashboard():
    return render_template("register/register.html")



@blueprint.route("/profile", methods=["GET", "POST"])
@validate_access
def profile():


    @validate_request()
    def post(data):
        pass

    if request.method == 'POST':
        post()

    return render_template("dashboard/profile.html")
