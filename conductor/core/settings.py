import os
import pathlib
from urllib.parse import quote

from pydantic import BaseSettings

BASE_DIR: str = str(pathlib.Path(__file__).parent.parent.parent)


class Settings(BaseSettings):
    app_title = 'Conductor'
    api_prefix = '/api'

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    mongo_auth_db: str
    mongo_db_name: str

    static_dir_path: str = os.path.join(BASE_DIR, 'static')
    templates_dir_path: str = os.path.join(BASE_DIR, 'templates')

    prod_mode: bool = False

    mailru_login: str
    mailru_password: str
    mailru_server: str = 'smtp.mail.ru'
    mailru_port: int = 465

    site_url: str = 'http://127.0.0.1:8081/auth'

    tg_bot_token: str
    tg_admin_ids: list[int]

    @property
    def mongo_uri(self) -> str:
        return (
            f'mongodb://{self.mongo_user}:{quote(self.mongo_password)}'
            f'@{self.mongo_host}:{self.mongo_port}/?authSource={self.mongo_auth_db}'
        )

    class Config:
        _env_file = os.path.join(BASE_DIR, '.env')
        if os.path.exists(_env_file):
            env_file = _env_file

    log_file: str = os.path.join(BASE_DIR, 'story.log')


settings = Settings()
