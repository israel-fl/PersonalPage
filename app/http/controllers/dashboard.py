from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user, login_required
from app.models.article import Article
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
        author = request.form.get("author")
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        slug = request.form.get("slug")
        # replace whitespace in slug with dashes and chagne to lowercase
        slug = slug.replace(' ', '-').lower()
        image = request.form.get("image")
        image_alt = request.form.get("image_alt")
        content = request.form.get("content")

        if (db.query(Article).filter(Article.title == title).first()):
            flash("Sorry there is already an article with that title", "danger")
        elif (db.query(Article).filter(Article.slug == slug).first()):
            flash("Sorry the slug is already in use, try changing it", "danger")
        else:
            try:
                article = Article(author=author,
                                  title=title,
                                  subtitle=subtitle,
                                  slug=slug,
                                  image=image,
                                  image_alt=image_alt,
                                  content=content
                                  )
                db.add(article)
                db.commit()
                flash("New article has been successfully created", "success")
            except Exception:
                db.rollback()
                flash("There was an error processing your request", "danger")

    if request.method == 'POST':
        post()
    return render_template("dashboard/create_article.html")
