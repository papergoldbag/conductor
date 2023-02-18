import logging

from conductor.testdata.insert_test_data import insert_test_data

log = logging.getLogger(__name__)


async def on_startup():
    ...


async def on_shutdown():
    pass
