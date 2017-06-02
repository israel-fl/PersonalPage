from flask import render_template, request, url_for, \
    Blueprint, abort
from app.models.blog import Post
from app.models.user import User

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
    articles = Post.query.order_by(Post.id.desc()).limit(6)
    # reverse the list so the latest one starts at 0
    articles = reversed(list(articles))
    # the 0 index will always be the latest article, which makes it
    # the featured article
    featured_article = articles[0].title
    featured_image = articles[0].featured_image_url
    featured_url = url_for("blog.show_entry", slug=articles[0].slug)
    featured_author = articles[0].author
    # remove the featured from the article list
    del articles[0]
    # create a dictionary that contains the rest of the articles
    article_dict = dict()
    for article in articles:
        article_dict.update({
                                "title": article.title,
                                "url": url_for("blog.show_entry", slug=article.slug),
                                "featured_image_url": article.featured_image_url,
                                "author": article.author
                            })

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

    # TODO IMPLEMENT A WAY FOR USERS TO COMMENT ARTICLES
    def post():
        pass

    if request.method == 'POST':
        post()

    article = Post.query.filter(Post.slug == slug).first()
    if article:
        # modify time crated to be in a readable format
        created = article.post_date
        time_string = created.strftime('%b %d, %Y')
        return render_template("blogging/article.html",
                               title=article.title,
                               author=article.author,
                               subtitle=article.subtitle,
                               image_url=article.featured_image_url,
                               content=article.content,
                               created=time_string,
                               )
    else:
        abort(404)

