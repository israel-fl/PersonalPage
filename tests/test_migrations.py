from alembic.command import upgrade, downgrade
from alembic.config import Config

ALEMBIC_CONFIG = '../database/alembic_test.ini'

# Apply migrations
def test_apply_migrations():
    """Applies all alembic migrations."""
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')

# Destroy migrations
def test_teardown_migrations():
    """Applies all alembic migrations."""
    config = Config(ALEMBIC_CONFIG)
    downgrade(config, 'base')

