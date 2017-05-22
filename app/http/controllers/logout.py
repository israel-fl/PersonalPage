from flask import render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_login import logout_user, login_required
from app.models.users import User, PasswordResetRequest
from database.db_adapter import db

blueprint = Blueprint('logout', __name__)


@blueprint.route("/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login"))
