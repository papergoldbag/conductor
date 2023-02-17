from starlette.templating import Jinja2Templates

from conductor.core.settings import Settings
from conductor.db.db import DB

settings = Settings()
templates = Jinja2Templates(directory=settings.templates_dir_path)
db = DB(settings.mongo_uri, settings.mongo_db_name)
