from flask import Flask
from app.http.controllers
from flask_socketio import SocketIO
import json
from flask_login import LoginManager, logout_user
from app.models.users import User
from database.db_adapter import db


socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = "26OxAJGy4r#FhIkiluQQrel$@EJcBi9b"
    app.config.SERVICE_NAME = "IsraelFL"
    with open("app/config.json") as config_file:
        keys = json.load(config_file)
        app.secret_key = keys.get("SECRET_KEY")
        app.config['MAIL_PASSWORD'] = keys.get("MAIL_PASS")
        app.config['MAIL_USERNAME'] = keys.get("MAIL_USERNAME")
        app.config['MAIL_PORT'] = keys.get("MAIL_PORT")
        app.config['MAIL_SERVER'] = keys.get("MAIL_SERVER")
        app.config['MAIL_USE_TLS'] = keys.get("MAIL_USE_TLS")
        app.config['MAIL_USE_SSL'] = keys.get("MAIL_USE_SSL")

    app.register_blueprint(controllers.home.blueprint)
    app.register_blueprint(controllers.users.blueprint, url_prefix='/users')
    app.register_blueprint(controllers.register.blueprint, url_prefix='/register')
    app.register_blueprint(controllers.login.blueprint, url_prefix='/login')
    app.register_blueprint(controllers.dashboard.blueprint, url_prefix='/dashboard')
    setup_authentication(app)
    socketio.init_app(app)
    return app


def setup_authentication(app):
    def load_user(user_id):
        user = db.query(User.id == user_id).first()
        if user:
            return user
    login_manager = LoginManager(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = 'login/login'
