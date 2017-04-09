# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import json

# with open("app/controllers/config.json") as config_file:
# # with open("C:\inetpub\Glacier\controllers\config.json") as config_file:
#     keys = json.load(config_file)
#     driver = keys.get("db_driver", "postgresql")
#     user = keys.get("db_user", "postgres")
#     password = keys.get("db_pass", "admin")
#     host = keys.get("db_host", "localhost")
#     port = keys.get("db_port", "5432")
#     name = keys.get("db_name", "development")

# engine = create_engine(
#     '{driver}://{user}:{password}@{db_host}:{port}/{db_name}'.format(
#         driver=driver,
#         user=user,
#         password=password,
#         db_host=host,
#         port=port,
#         db_name=name
#     )
# )

# Session = sessionmaker(bind=engine)

# db = Session()

# Base = declarative_base()

# Base.metadata.create_all(engine)
