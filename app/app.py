from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from time import sleep
from sqlalchemy.orm import load_only
from sqlalchemy import desc
from functools import wraps
import json


app = Flask(__name__)
socketio = SocketIO(app)
with open("../config.json") as config_file:
    keys = json.load(config_file)
    app.secret_key = keys.get("SECRET_KEY")
    app.config['MAIL_PASSWORD'] = keys.get("MAIL_PASS")
    app.config['MAIL_USERNAME'] = keys.get("MAIL_USERNAME")
    app.config['MAIL_PORT'] = keys.get("MAIL_PORT")
    app.config['MAIL_SERVER'] = keys.get("MAIL_SERVER")
    app.config['MAIL_USE_TLS'] = keys.get("MAIL_USE_TLS")
    app.config['MAIL_USE_SSL'] = keys.get("MAIL_USE_SSL")

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.route("/", methods=["GET", "POST"])
def landing():
    if (request.method == "POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        mail = Mail(app)
        email = Message(
                subject="A new message from IsraelFL!",
                sender="iflore04@gmail.com",
                recipients=email)
        email.html = render_template("emails/contact_email.html",
                                     name=name,
                                     email=email,
                                     phone=phone,
                                     message=message)

        mail.send(email)

    return render_template("main/index.html")


@app.route("/resume", methods=["GET"])
def show_resume():
    return render_template("main/resume.html")


@socketio.on('message', namespace='/test')
def handle_message(message):
    emit('MESSAGE', {'data': message['data'], 'user': 'SAMMY', 'position': 'left'}, broadcast=True)


@socketio.on('broadcast', namespace='/test')
def test_message(message):
    emit('MESSAGE', {'data': message['data'], 'user': "visitor", 'position': 'right'}, broadcast=True)
