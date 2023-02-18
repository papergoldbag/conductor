import logging

from conductor.core.misc import db, settings
from conductor.testdata.insert_test_data import insert_test_data

log = logging.getLogger(__name__)


async def on_startup():
    if settings.prod_mode:
        insert_test_data()
    db.ensure_indexes()


async def on_shutdown():
    pass
