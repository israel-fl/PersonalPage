from flask import Flask
from app.http.controllers import home, login, register, users, dashboard
from flask_socketio import SocketIO
import json
from flask_login import LoginManager, logout_user
from app.models.users import User
from database.db_adapter import db
from flask_mail import Mail, Message

socketio = SocketIO()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.secret_key = "26OxAJGy4r#FhIkiluQQrel$@EJcBi9b"
    app.config.SERVICE_NAME = "IsraelFL"
    with open("app/config.json") as config_file:
        keys = json.load(config_file)
        app.secret_key = keys.get("SECRET_KEY")
        app.config['MAIL_PASSWORD'] = keys.get("MAIL_PASSWORD")
        app.config['MAIL_USERNAME'] = keys.get("MAIL_USERNAME")
        app.config['MAIL_PORT'] = keys.get("MAIL_PORT")
        app.config['MAIL_SERVER'] = keys.get("MAIL_SERVER")
        app.config['MAIL_USE_TLS'] = keys.get("MAIL_USE_TLS")
        app.config['MAIL_USE_SSL'] = keys.get("MAIL_USE_SSL")
        if (keys.get("SERVICE_MODE") == "DEVELOPMENT"):
            app.config['DEBUG'] = True
            app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.register_blueprint(home.blueprint)
    app.register_blueprint(register.blueprint, url_prefix='/register')
    app.register_blueprint(login.blueprint, url_prefix='/login')
    app.register_blueprint(dashboard.blueprint, url_prefix='/dashboard')
    setup_authentication(app)
    mail.init_app(app)
    socketio.init_app(app)
    return app


def setup_authentication(app):
    def load_user(user_id):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    login_manager = LoginManager(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = 'login.login'
