import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from conductor.api.v1 import api_v1_router
from conductor.core.events import on_startup, on_shutdown
from conductor.core.settings import settings
from conductor.core.setup_logging import setup_logging

log = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.app_title)

    if not os.path.exists(settings.static_dir_path):
        os.mkdir(settings.static_dir_path)
        log.info('static dir was created')
    if not settings.prod_mode:
        app.mount("/static", StaticFiles(directory=settings.static_dir_path), name="static")
        log.info('FastAPI app StaticFiles was activated')

    if not os.path.exists(settings.templates_dir_path):
        os.mkdir(settings.templates_dir_path)
        log.info('templates dir was created')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)

    app.include_router(api_v1_router, prefix=settings.api_prefix)

    return app
