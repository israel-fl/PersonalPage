from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from time import sleep
from controllers.db_adapter import db
import json
import requests
from sqlalchemy.orm import load_only
import datetime
from sqlalchemy import desc
from functools import wraps
import hashlib


VERSION = 0.1
app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.route("/", methods=["GET"])
def landing():

    return render_template("main/index.html")


if __name__ == "__main__":

    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
