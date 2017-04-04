from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from time import sleep
from controllers.db_adapter import db
from models.tables import Group, Managed, Upload, GlobalGroup, Retrieval
import json
import requests
from sqlalchemy.orm import load_only
import datetime
from sqlalchemy import desc
from functools import wraps
import hashlib


REGION_NAME = "us-east-1"
VERSION = 0.9
DOWN_REVISION = 0.5
app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.route("/Glacier/", methods=["GET"])
def landing():

    return render_template("main/landing.html")


if __name__ == "__main__":

    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
