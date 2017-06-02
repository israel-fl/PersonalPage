from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Message
from flask_login import logout_user, login_user, current_user


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
        message = request.form.get("message")
        send_message_email(name, email_addr, phone, message)
        flash("Message sent successfully, I typically reply to messages within 24 hours.", "success")

    if (request.method == "POST"):
        post()
    return render_template("home/contact.html")
