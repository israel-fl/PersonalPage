from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Message
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.security import generate_password_hash
from database.db_adapter import db
from app.models.user import User

blueprint = Blueprint('home', __name__)


@blueprint.route("/", methods=["GET"])
def landing():
    return render_template("home/home.html")


@blueprint.route("/contact", methods=["GET", "POST"])
def contact():

    def post():
        from app.http.controllers.mail_senders import send_message_email
        name = request.form.get("name")
        email_addr = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("content")
        send_message_email(name, email_addr, phone, message)
        flash("Message sent successfully, I typically reply to messages within 24 hours.", "success")

    if (request.method == "POST"):
        post()
    return render_template("home/contact.html")


@blueprint.route("/account", methods=["GET", "POST"])
@login_required
def account():

    def post():
        name = request.form.get("name")
        password = generate_password_hash(request.form.get('password'))
        user = User.query.filter(User.id == current_user.id).first()
        user.name = name
        user.password = password
        try:
            # save changes to the user
            db.commit()
            flash("Changes saved successfully", "success")
        except Exception:
            db.rollback()
            flash("There was an error processing your request", "danger")
    # Determine the request type
    if request.method == "POST":
        return post()
    return render_template("home/account.html",
                           name=current_user.name,
                           profile_image_url=current_user.profile_image_url)
