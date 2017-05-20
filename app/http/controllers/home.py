from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Message


blueprint = Blueprint('home', __name__)

@blueprint.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@blueprint.route("/", methods=["GET", "POST"])
def landing():
    if (request.method == "POST"):
        from app.http.controllers.mail_senders import send_message_email
        name = request.form.get("name")
        email_addr = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        send_message_email(name, email_addr, phone, message)

    return render_template("main/index.html")
