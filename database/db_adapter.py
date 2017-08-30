from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import json


with open("/home/israel/Documents/PersonalPage/env.json") as config_file:
    keys = json.load(config_file)

# Create an engine using the specified configurations
engine = create_engine(keys.get("DB_URI"))


# store the seesion in an easy to remember variable
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))
Base = declarative_base()
Base.query = db.query_property()
meta = MetaData()


# Connect to the database
def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models
    meta.create_all(bind=engine)
