# from flask import Flask
# import json


# def create_app():
#     app = Flask(__name__)
#     with open("config.json") as config_file:
#         keys = json.load(config_file)
#         app.secret_key = keys.get("SECRET_KEY")
#         app.config['MAIL_PASSWORD'] = keys.get("MAIL_PASS")
#         app.config['MAIL_USERNAME'] = keys.get("MAIL_USERNAME")
#         app.config['MAIL_PORT'] = keys.get("MAIL_PORT")
#         app.config['MAIL_SERVER'] = keys.get("MAIL_SERVER")
#         app.config['MAIL_USE_TLS'] = keys.get("MAIL_USE_TLS")
#         app.config['MAIL_USE_SSL'] = keys.get("MAIL_USE_SSL")
#     return app
