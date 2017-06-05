from flask import render_template, request, url_for, \
    Blueprint, abort, Markup, flash
from app.models.blog import Post, Comment
from app.models.user import User
from app.models.pagination import Pagination
from markdown import markdown
from flask_login import login_required, current_user
from database.db_adapter import db

blueprint = Blueprint('blog', __name__)

PER_PAGE = 20


# Schema for an Article object
# {
#     "title": "article_title",
#     "url": "article url",
#     "featured_image_url": "url for image",
#     "author": "alt image title"
# }
@blueprint.route("/", methods=["GET", "POST"], defaults={'page': 1})
@blueprint.route('/page/<int:page>')
def index(page):

    def post():
        query = request.form.get("search")
        search_query = "%{}%".format(query)
        articles = Post.query.filter(Post.title.like(search_query)).all()
        # create a dictionary that contains the rest of the articles
        article_list = build_article_list(articles)
        return render_template("blogging/search_results.html",
                               articles=article_list,
                               search=query)

    # Get the latest 6 articles in the blog
    articles = Post.query.order_by(Post.id.desc()).all()
    total_articles = len(articles)
    pagination = Pagination(page, PER_PAGE, total_articles)
    article_list = build_article_list(articles)

    if request.method == 'POST':
        return post()

    return render_template("blogging/index.html",
                           articles=article_list,
                           pagination=pagination)


def build_article_list(articles):
    # create a dictionary that contains the rest of the articles
    article_list = list()
    for article in articles:
        article_list.append({
                                "title": article.title,
                                "url": url_for("blog.show_entry", slug=article.slug),
                                "featured_image_url": article.featured_image_url,
                                "content": article.content[0:300] + "..."
                            })
    return article_list


@blueprint.route("/<slug>", methods=["GET", "POST"])
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
                               profile_image_url=article.author.profile_image_url,
                               author_description=article.author.description,
                               subtitle=article.subtitle,
                               image_url=article.featured_image_url,
                               content=Markup(markdown(article.content)),
                               created=time_string,
                               slug=article.slug,
                               comments=article.comments
                               )
    else:
        abort(404)

