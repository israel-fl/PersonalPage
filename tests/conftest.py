import pytest
from app import create_app
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from alembic.command import upgrade, downgrade
from alembic.config import Config

ALEMBIC_CONFIG = '../database/alembic_test.ini'


@pytest.fixture(scope='session')
def db(request):
    # Initialize Database
    with open("/home/israel/Documents/PersonalPage/env.json") as config_file:
        keys = json.load(config_file)

    # Create an engine using the specified configurations
    engine = create_engine(keys.get("TEST_DB_URI"))


    # store the session in an easy to remember variable
    db = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))
    Base = declarative_base()
    Base.query = db.query_property()
    meta = MetaData()

    # Connect to the database
    import app.models
    meta.create_all(bind=engine)

    def teardown():
        db.remove()
    request.addfinalizer(teardown)
    return db



@pytest.fixture(scope='session')
def app(db, request):
    """Session-wide test `Flask` application."""
    app = create_app(testing=True)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        print("Teardown app")
        db.rollback()
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def session(db, request):

    def teardown():
        # Revert any changes made to the database
        db.rollback()

    request.addfinalizer(teardown)
    return session


# Reapply to leave database in working order
def test_apply_migrations_for_testing():
    """Applies all alembic migrations."""
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')
