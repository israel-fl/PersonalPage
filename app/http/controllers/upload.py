import os
from flask import render_template, request, flash, redirect, url_for, \
    Blueprint, current_app as app
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
from app.http.controllers.file_extension import allowed_file
import json


blueprint = Blueprint('upload', __name__)

'''
 Schema for image list

    {
        "name": "rm_lock.png",
        "path": "/static/images/blog/rm_lock.png"
    }

'''


@blueprint.route('/', methods=['GET', 'POST'])
def upload_file():
    upload_folder = app.config['UPLOAD_FOLDER']

    def post():
        # check if the post request has a file
        if 'file' not in request.files:
            flash('No file selected', "info")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            flash("File uploaded successfully", "success")
        else:
            flash("Sorry that file type is not allowed", "danger")

    if request.method == 'POST':
        post()

    images = list()
    image_list = [f for f in listdir(upload_folder) if isfile(join(upload_folder, f))]
    for image in image_list:
        images.append({
                            "name": image,
                            "path": "http://localhost:8080/static/images/blog/{}".format(image)
                          })
    return render_template("blogging/fileupload.html", images=json.dumps(images))


@blueprint.route('/delete/<file>', methods=['GET'])
def delete_file(file):
    print(file)
    return redirect(url_for("upload.upload_file"))