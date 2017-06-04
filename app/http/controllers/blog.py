from flask import render_template, request, url_for, \
    Blueprint, abort, Markup, flash
from app.models.blog import Post, Comment
from app.models.user import User
from markdown import markdown
from flask_login import login_required, current_user
from database.db_adapter import db

blueprint = Blueprint('blog', __name__)


# Schema for an Article object
# {
#     "title": "article_title",
#     "url": "article url",
#     "featured_image_url": "url for image",
#     "author": "alt image title"
# }

@blueprint.route("/", methods=["GET"])
def index():
    # Get the latest 6 articles in the blog
    articles = Post.query.order_by(Post.id.desc()).limit(6).all()
    # create a dictionary that contains the rest of the articles
    article_dict = dict()
    for counter, article in enumerate(articles):
        print(counter, article)
        if counter != 0:
            article_dict.update({
                                    "title": article.title,
                                    "url": url_for("blog.show_entry", slug=article.slug),
                                    "featured_image_url": article.featured_image_url,
                                    "author": article.author
                                })
        else:
            featured_article = article.title
            featured_image = article.featured_image_url
            featured_url = url_for("blog.show_entry", slug=article.slug)
            featured_author = article.author.name

    return render_template("blogging/index.html",
                           featured_article=featured_article,
                           featured_image=featured_image,
                           featured_url=featured_url,
                           featured_author=featured_author,
                           articles=article_dict)


# DO I really want this?
@blueprint.route("/sitemap", methods=["GET"])
def  sitemap():
    return render_template('blogging/sitemap.html')


@blueprint.route("/<slug>", methods=["GET"])
def show_entry(slug):

    article = Post.query.filter(Post.slug == slug).first()

    def post():

        title = request.form.get("title")
        content = request.form.get("comment")
        user_id = current_user.id
        post_id = article.id
        comment = Comment(title=title,
                          comment=content,
                          user_id=user_id,
                          post_id=post_id)
        try:
            db.add(comment)
            db.commit()
            flash("Comment added successfully", "success")
        except Exception:
            db.rollback()
            flash("There was an error processing your request", "danger")


    if request.method == 'POST':
        post()

    if article:
        # modify time crated to be in a readable format
        created = article.created
        time_string = created.strftime('%b %d, %Y')
        return render_template("blogging/article.html",
                               title=article.title,
                               author=article.author.name,
                               subtitle=article.subtitle,
                               image_url=article.featured_image_url,
                               content=Markup(markdown(article.content)),
                               created=time_string,
                               slug=article.slug
                               )
    else:
        abort(404)

