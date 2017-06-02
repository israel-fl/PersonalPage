from flask import render_template, request, flash, Blueprint
from flask_login import current_user, login_required
from app.models.user import User
from database.db_adapter import db
from werkzeug.security import generate_password_hash


blueprint = Blueprint('account', __name__)


@blueprint.route("/", methods=["GET", "POST"])
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
    return render_template("home/account.html")
