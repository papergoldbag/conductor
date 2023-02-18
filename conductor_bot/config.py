from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class DB:
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    mongo_auth_db: str
    db_name: str


@dataclass
class User:
    username: str
    chat_id: str
    id: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous

