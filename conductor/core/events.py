import logging

from conductor.core.misc import settings
from conductor.testdata.insert_test_data import insert_test_data

log = logging.getLogger(__name__)


async def on_startup():
    if settings.prod_mode:
        insert_test_data()


async def on_shutdown():
    pass
