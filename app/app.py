from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_from_directory, Mail, Message
from flask_socketio import SocketIO, emit
from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from time import sleep
# from controllers.db_adapter import db
from sqlalchemy.orm import load_only
from sqlalchemy import desc
from functools import wraps


VERSION = 0.1
app = Flask(__name__)
socketio = SocketIO(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'iflore04@gmail.com'
app.config['MAIL_PASSWORD'] = 'ce651edaf59be5ef2badb77d2833f3feac9fbab8abd4cc8b5e1af7921f58a9db'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

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
        pass
    return render_template("main/index.html")


@app.route("/resume", methods=["GET"])
def show_resume():
    return render_template("main/resume.html")


@app.route('/resume/download', methods=['GET'])
def download():
    return send_from_directory(url_for("static", filename="work_resume.pdf"))


@app.route('/data', methods=["GET"])
def render():
    return render_template("main/data.html")


@socketio.on('message', namespace='/test')
def handle_message(message):
    emit('MESSAGE', {'data': message['data'], 'user': 'SAMMY', 'position': 'left'}, broadcast=True)

@socketio.on('broadcast', namespace='/test')
def test_message(message):
    emit('MESSAGE', {'data': message['data'], 'user': "visitor", 'position': 'right'}, broadcast=True)

if __name__ == "__main__":

    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
