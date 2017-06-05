from flask import Flask, request, url_for
from app.http.controllers import home, login, register, dashboard,\
    logout, blog, upload, account
from flask_socketio import SocketIO
import json
from database.db_adapter import db, init_db
from flask_mail import Mail
from flask_login import LoginManager
from app.models.user import User


socketio = SocketIO()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.secret_key = "26OxAJGy4r#FhIkiluQQrel$@EJcBi9b"
    app.config.SERVICE_NAME = "IsraelFL"

    # Init database
    init_db()

    with open("app/config.json") as config_file:
        keys = json.load(config_file)
        app.secret_key = keys.get("SECRET_KEY")
        app.config['MAIL_PASSWORD'] = keys.get("MAIL_PASSWORD")
        app.config['MAIL_USERNAME'] = keys.get("MAIL_USERNAME")
        app.config['MAIL_PORT'] = keys.get("MAIL_PORT")
        app.config['MAIL_SERVER'] = keys.get("MAIL_SERVER")
        app.config['MAIL_USE_TLS'] = keys.get("MAIL_USE_TLS")
        app.config['MAIL_USE_SSL'] = keys.get("MAIL_USE_SSL")
        # For File uploading #
        app.config['UPLOAD_FOLDER'] = keys.get("UPLOAD_FOLDER")
        if (keys.get("SERVICE_MODE") == "DEVELOPMENT"):
            app.config['DEBUG'] = True
            app.config["TEMPLATES_AUTO_RELOAD"] = True

    # BLUEPRINTS
    app.register_blueprint(home.blueprint)
    app.register_blueprint(register.blueprint, url_prefix='/register')
    app.register_blueprint(login.blueprint, url_prefix='/login')
    app.register_blueprint(dashboard.blueprint, url_prefix='/dashboard')
    app.register_blueprint(logout.blueprint, url_prefix='/logout')
    app.register_blueprint(blog.blueprint, url_prefix='/blog')
    app.register_blueprint(upload.blueprint, url_prefix='/upload')
    app.register_blueprint(account.blueprint, url_prefix='/account')

    # LOGIN SETUP
    setup_authentication(app)

    # Mail
    mail.init_app(app)

    # SocketIO
    socketio.init_app(app)

    # Url generator
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page

    return app


def setup_authentication(app):
    def load_user(user_id):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    login_manager = LoginManager(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = 'login.login'


# Url generator
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
