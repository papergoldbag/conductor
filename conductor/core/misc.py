from starlette.templating import Jinja2Templates

from conductor.core.settings import Settings

settings = Settings()
templates = Jinja2Templates(directory=settings.templates_dir_path)
