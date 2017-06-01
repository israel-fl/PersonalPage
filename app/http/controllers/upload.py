from flask import render_template, request, flash, redirect, url_for,\
 Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import logout_user, login_user, current_user
from app.models.user import User, PasswordResetRequest
from database.db_adapter import db
from werkzeug.security import check_password_hash
from app.http.middleware.generators import generate_hash
from werkzeug.utils import secure_filename
import os
from app.http.controllers.file_extension import allowed_file


blueprint = Blueprint('upload', __name__)


@blueprint.route('/', methods=['POST'])
def upload_file():

    def post():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    if request.method == 'POST':
        return post()
    pass
