from flask import Markup
from flask import render_template, request, flash, Blueprint
from flask_login import login_required, current_user
from markdown import markdown
from werkzeug.security import generate_password_hash

from app.models.blog import Post
from app.models.user import User
from database.db_adapter import db

blueprint = Blueprint('dashboard', __name__)


@blueprint.route("/", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")


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
        author = current_user.name
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        # turn the title into a slug
        slug = title.replace(' ', '-').lower()
        featured_image_url = request.form.get("featured-image")  # get image url
        content = request.form.get("content")
        tags = request.form.get("tags")

        if (Post.query.filter(Post.title == title).first()):
            flash("Sorry there is already an article with that title", "danger")
        else:
            try:
                post = Post(
                            author=author,
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
    return render_template("blogging/editor.html")


@blueprint.route("/parse", methods=["POST"])
def parse_markdown():
    content = request.form.get("content")
    content = Markup(markdown(content))
    return content
