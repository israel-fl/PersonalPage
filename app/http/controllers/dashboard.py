from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user, login_required, current_user
from app.models.blog import Post, UserPost
from database.db_adapter import db
from app.http.middleware.decorators import validate_request, validate_access
from werkzeug.security import generate_password_hash


blueprint = Blueprint('dashboard', __name__)


@blueprint.route("/", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")


@blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    def post():
        pass

    if request.method == 'POST':
        post()

    return render_template("dashboard/profile.html")


@blueprint.route("/create-article", methods=["GET", "POST"])
@login_required
def create_article():

    def post():
        author = current_user.name
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        # turn the title into a slug
        slug = title.replace(' ', '-').lower()
        featured_image_url = ""  # get image url
        content = request.form.get("content")
        tags = request.form.get("tags")
        draft = request.form.get("draft")

        if (Post.query.filter(Post.title == title).first()):
            flash("Sorry there is already an article with that title", "danger")
        else:
            try:
                article = Post(author=author,
                               title=title,
                               content=content,
                               draft=draft,
                               tags=tags,
                               subtitle=subtitle,
                               slug=slug,
                               featured_image_url=featured_image_url)
                # add article to database
                db.add(article)
                db.commit()
                user_post = UserPost(user_id=current_user.id,
                                     post_id=article.id)
                # establish a relationship between post and user
                db.add(user_post)
                db.commit()
                flash("New article has been successfully created", "success")
            except Exception:
                db.rollback()
                flash("There was an error processing your request", "danger")

    if request.method == 'POST':
        post()
    return redirect(url_for("blogging.editor"))
