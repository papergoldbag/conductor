from pymongo import MongoClient

from conductor.db.collections_.user import UserCollection


class DB:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.database = self.client.get_database(db_name)

    @property
    def user(self) -> UserCollection:
        return UserCollection(self.database.get_collection('user'))
