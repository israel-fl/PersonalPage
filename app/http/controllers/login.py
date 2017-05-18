from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user
from app.models.users import User
from database.db_adapter import db


blueprint = Blueprint('login', __name__)

login_manager = LoginManager(app)

@blueprint.route("/", methods=["GET", "P"])
def login():


    def post():
        pass

    # Determine the request type
    if (request.method == "POST"):
        post()

    return render_template("login/login.html")


@login_manager.user_loader
def load_user(user_id):
    return db.query(User.__id == user_id)
