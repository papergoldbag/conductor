from conductor_bot.settings import config_bd, mongo_uri
from conductor.db.db import DB
from pymongo.cursor import Cursor
import emoji

async def check_user_system(user_tg: str):
    user = db.user.pymongo_collection.find_one({"telegram": user_tg})
    user_with_prefix = db.user.pymongo_collection.find_one({"telegram": "https://t.me/" + user_tg})
    return user is not None or user_with_prefix is not None


def desc(user):
    return emoji.emojize(
        f"Имя: {user['fullname']} :man_student:\nemail: {user['email']} :love_letter:\nОписание: {user['position']} :hammer_and_wrench:\ntelegram: {user['telegram']} :speech_balloon:"
    )


def get_user_description(user_tg: str):
    data_params = {"_id": 0, "fullname": 1, "email": 1, "position": 1, "telegram": 1}
    user = db.user.pymongo_collection.find_one({"telegram": user_tg}, data_params)
    user_with_prefix = db.user.pymongo_collection.find_one({"telegram": "https://t.me/" + user_tg}, data_params)
    if user is not None:
        return desc(user)
    else: 
        return desc(user_with_prefix)

db = DB(mongo_uri, config_bd.db.db_name)
