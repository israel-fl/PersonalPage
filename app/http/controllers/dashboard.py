from flask import render_template, request, flash, Blueprint, url_for,\
    Markup, abort, redirect
from flask_login import login_required, current_user, logout_user
from markdown import markdown
from werkzeug.security import generate_password_hash
from app.models.blog import Post
from app.models.user import User
from database.db_adapter import db
import json
import re
from app.http.middleware.decorators import validate_access

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
@validate_access(2)
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
@validate_access(2)
def profile():

    def post():
        user = User.query.filter(User.id == current_user.id).first()

        if (int(request.form.get("form-type")) == 1):
            print("Form type 1")
            user.name = request.form.get("name")
            user.description = request.form.get("description")
        else:
            print("Form type 2")
            password = generate_password_hash(request.form.get('password'))
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
                           description=current_user.description
                           )


@blueprint.route("/create-article", methods=["GET", "POST"])
@validate_access(2)
def create_article():

    def post():
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        # turn the title into a slug by removing all non alphanumeric or numeric
        # characters
        slug = re.sub(r'[^a-zA-Z0-9]', '-', title)
        # make it all lowercase
        slug = slug.lower()
        print(slug)
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
@validate_access(2)
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


@blueprint.route("/approvals", methods=["GET"])
@validate_access(3)
def show_pending_approvals():

    article_list = list()
    articles = Post.query.filter(Post.published == False).all()
    print(articles)
    if articles:
        for article in articles:
            article_list.append({
                                    "created": article.created.strftime('%b %d, %Y'),
                                    "title": article.title,
                                    "author": article.author.name,
                                    "slug": article.slug
                                })

    return render_template("dashboard/approvals.html", articles=article_list)


@blueprint.route("/approvals/<slug>", methods=["GET"])
@validate_access(3)
def approve(slug):

    article = Post.query.filter(Post.slug == slug).first()
    if article:
        article.published = True
        try:
            db.commit()
            flash("Article approved", "success")
        except Exception:
            db.rollback()
            flash("There was an error processing your request", "danger")
    else:
        abort(404)

    return redirect(url_for("dashboard.show_pending_approvals"))


@blueprint.route("/create", methods=["GET", "POST"])
@validate_access(3)
def create_admin():

    def post():
        try:
            password = generate_password_hash(request.form.get('password'))
            email = request.form.get("email")
            name = request.form.get("name")
            username = request.form.get("username")
            # Check if an account with the given credentials already exists
            if (User.query.filter(User.email == email).first()):
                flash('Sorry, there is already an account associated with that email', "danger")
            elif (User.query.filter(User.display_name == username).first()):
                flash('Sorry, that username has already been taken', "danger")
            else:
                user = User(name=name,
                            display_name=username,
                            email=email,
                            password=password,
                            profile_image_url=url_for('static', filename='images/default_logo.png'))
                # save the new user
                db.add(user)
                db.commit()

                # check if there is a user logged in, if so log them out
                if (current_user):
                    logout_user()
                # login the current user so that we have a handle on the object
                from app.http.controllers.mail_senders import send_verify_email
                send_verify_email(user)
                flash("The user was created successfully and a verification email has been sent", "success")
        except Exception as e:
            print(e)
            db.rollback()
            flash("There was an error processing your request", "danger")

    if request.method == 'POST':
        post()

    return render_template("dashboard/create_user.html")

# Parse markdown content
@blueprint.route("/parse", methods=["POST"])
@validate_access(2)
def parse_markdown():
    content = request.form.get("content")
    content = Markup(markdown(content))
    return content
