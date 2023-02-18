import logging

from conductor.core.misc import settings, db
from conductor.testdata.insert_test_data import insert_test_data

log = logging.getLogger(__name__)


async def on_startup():
    print(1)
    insert_test_data()
    db.ensure_indexes()


async def on_shutdown():
    pass
