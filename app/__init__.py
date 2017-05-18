from flask import Flask
from app.http.controllers import home, users, login
from flask_socketio import SocketIO
import json
from flask_login import LoginManager, logout_user


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

    app.register_blueprint(home.blueprint)
    app.register_blueprint(users.blueprint, url_prefix='/users')
    app.register_blueprint(login.blueprint, url_prefix='/login')
    socketio.init_app(app)
    return app


def setup_authentication(app):
    def load_account(account_id):
        account = controllers.db.users.find_one(account_id)
        if account:
            return User(account)
    login_manager = LoginManager(app)
    login_manager.user_loader(load_account)
    login_manager.login_view = 'home.login'
