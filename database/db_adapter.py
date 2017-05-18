from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

with open("database/config.json") as config_file:
    keys = json.load(config_file)
    driver = keys.get("db_driver")
    user = keys.get("db_user")
    password = keys.get("db_pass")
    host = keys.get("db_host")
    port = keys.get("db_port")
    name = keys.get("db_name")

# Create an engine using the specified configurations
engine = create_engine(
    '{driver}://{user}:{password}@{db_host}:{port}/{db_name}'.format(
        driver=driver,
        user=user,
        password=password,
        db_host=host,
        port=port,
        db_name=name
    )
)

# Connect to the database
Session = sessionmaker(bind=engine)

# store the seesion in an easy to remember variable
db = Session()

Base = declarative_base()

Base.metadata.create_all(engine)
