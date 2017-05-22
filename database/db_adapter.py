import json
from flask_blogging import SQLAStorage
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy


def get_uri():
    with open("database/config.json") as config_file:
        keys = json.load(config_file)
        driver = keys.get("db_driver")
        user = keys.get("db_user")
        password = keys.get("db_pass")
        host = keys.get("db_host")
        port = keys.get("db_port")
        name = keys.get("db_name")

    # Create an engine using the specified configurations
    db_uri = '{driver}://{user}:{password}@{db_host}:{port}/{db_name}'.format(
            driver=driver,
            user=user,
            password=password,
            db_host=host,
            port=port,
            db_name=name
        )
    return db_uri
