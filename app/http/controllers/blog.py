from flask import Flask, render_template, request, flash, redirect, url_for,\
    jsonify, send_from_directory, Blueprint, abort, current_app as app
from flask_mail import Mail, Message
from flask_login import LoginManager, logout_user, login_required
from app.models.article import Article
from database.db_adapter import db
from app.http.middleware.decorators import validate_request, validate_access
from werkzeug.security import generate_password_hash


blueprint = Blueprint('blog', __name__)


# Schema for an Article object
# {
#     "title": "article_title",
#     "url": "article url",
#     "image_url": "url for image",
#     "image_alt": "alt image title"
# }

@blueprint.route("/", methods=["GET"])
def blog():
    # Get the latest 6 articles in the blog
    articles = db.query(Article).order_by(Article.id.desc()).limit(6)
    # reverse the list so the latest one starts at 0
    articles = reversed(articles)
    # the 0 index will always be the latest article, which makes it
    # the featured article
    featured_article = articles[0].title
    featured_image = articles[0].image_url
    featured_image_alt = articles[0].image_alt
    # remove the featured from the article list
    del articles[0]
    # create a dictionary that contains the rest of the articles
    article_dict = dict()
    for article in articles:
        article_dict.update({
                                "title": article.title,
                                "url": url_for("blog.show_entry", slug=article.slug),
                                "image_url": article.image_url,
                                "image_alt": article.image_alt
                            })

    return render_template("blog/blog.html",
                           featured_article=featured_article,
                           featured_image=featured_image,
                           featured_image_alt=featured_image_alt,
                           articles=article_dict)


@blueprint.route("/<slug>", methods=["GET"])
def show_entry(slug):

    # TODO IMPLEMENT A WAY FOR USERS TO COMMENT ARTICLES
    def post():
        pass

    if request.method == 'POST':
        post()

    article = db.query(Article).filter(Article.slug == slug).first()
    if (article):
        # modify time crated to me in a readable format
        created = article.created
        return render_template("blog/post.html",
                               title=article.title,
                               author=article.author,
                               subtitle=article.subtitle,
                               content=article.content,
                               created=created,
                               image_url=article.image_url,
                               image_alt=article.image_alt
                               )
    else:
        abort(404)

