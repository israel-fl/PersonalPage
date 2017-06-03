from flask import Markup
from flask import render_template, request, flash, Blueprint, url_for, redirect
from flask_login import login_required, current_user
from markdown import markdown
from werkzeug.security import generate_password_hash
from app.models.blog import Post
from app.models.user import User
from database.db_adapter import db
import json
import re

blueprint = Blueprint('dashboard', __name__)


'''
 Schema for article list

    {
        "created": "date",
        "title": "My first awesome Blog",
        "comments": 50,
        "url": "article url",
        "slug": "article slug
    }
'''


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def dashboard():

    def post():
        pass

    if request.method == 'POST':
        post()

    article_list = list()
    articles = Post.query.filter(Post.user_id == current_user.id).all()
    print(articles)
    if articles:
        for article in articles:
            article_list.append({
                                    "created": article.created.strftime('%b %d, %Y'),
                                    "title": article.title,
                                    "comments": len(article.comments),
                                    "url": url_for("blog.show_entry", slug=article.slug),
                                    "slug": article.slug
                                })

    return render_template("dashboard/dashboard.html",
                           articles=json.dumps(article_list))


@blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

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

    if request.method == 'POST':
        post()

    return render_template("dashboard/profile.html",
                           username=current_user.display_name,
                           name=current_user.name,
                           profile_image_url=current_user.profile_image_url,
                           )


@blueprint.route("/create-article", methods=["GET", "POST"])
@login_required
def create_article():

    def post():
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        # turn the title into a slug by removing all non alphanumeric or numeric
        # characters
        slug = re.sub(r'[^a-zA-Z0-9]', '-', title)
        # make it all lowercase
        slug = slug.lower()
        featured_image_url = request.form.get("featured-image")  # get image url
        content = request.form.get("content")
        tags = request.form.get("tags")

        if Post.query.filter(Post.title == title).first():
            flash("Sorry there is already an article with that title", "danger")
        else:
            try:
                post = Post(
                            user_id=current_user.id,
                            title=title,
                            subtitle=subtitle,
                            content=content,
                            featured_image_url=featured_image_url,
                            slug=slug,
                            tags=tags)
                # add article to database
                db.add(post)
                db.commit()

                flash("New article has been successfully created", "success")
            except Exception:
                db.rollback()
                flash("There was an error processing your request", "danger")

    if request.method == 'POST':
        post()
    return render_template("dashboard/editor.html")


@blueprint.route("/edit/<slug>", methods=["GET", "POST"])
@login_required
def edit_entry(slug):

    def post():
        article = Post.query.filter(Post.slug == slug).first()
        title = request.form.get("title")
        # if the title changed, check if there is already an article with the
        # new title
        if article.title != title:
            new_slug = title.replace(' ', '-').lower()
            existing_article = Post.query.filter(Post.slug == new_slug)
            if existing_article:
                flash("Sorry there is already an article with that title, try a different one", "danger")
                return

        article.subtitle = request.form.get("subtitle")
        article.slug = title.replace(' ', '-').lower()
        # turn the title into a slug
        article.featured_image_url = request.form.get("featured-image")  # get image url
        article.content = request.form.get("content")
        article.tags = request.form.get("tags")

        try:
            # Save changes
            db.commit()

            flash("Edits successfully saved", "success")
        except Exception:
            db.rollback()
            flash("There was an error processing your request", "danger")

    if request.method == 'POST':
        post()

    slug = Post.query.filter(Post.slug == slug).first()
    return render_template("dashboard/edit_post.html",
                           title=slug.title,
                           subtitle=slug.subtitle,
                           content=slug.content,
                           featured_image_url=slug.featured_image_url,
                           slug=slug.slug,
                           tags=slug.tags
                           )


@blueprint.route("/parse", methods=["POST"])
@login_required
def parse_markdown():
    content = request.form.get("content")
    content = Markup(markdown(content))
    return content
