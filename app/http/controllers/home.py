from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message


blueprint = Blueprint('home', __name__)

@blueprint.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@blueprint.route("/", methods=["GET", "POST"])
def landing():
    if (request.method == "POST"):
        name = request.form.get("name")
        email_addr = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        mail = Mail(app)
        email = Message(
                subject="A new message from {}!".format(name),
                sender="data.rhino@gmail.com",
                recipients=["iflore04@gmail.com"])
        email.html = render_template("emails/contact_email.html",
                                     name=name,
                                     email=email_addr,
                                     phone=phone,
                                     message=message)
        mail.send(email)

    return render_template("main/index.html")


@blueprint.route("/blog", methods=["GET"])
def blog():
    return render_template("main/blog.html")


@blueprint.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("main/dashboard.html")

