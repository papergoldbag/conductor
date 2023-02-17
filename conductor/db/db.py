from pymongo import MongoClient

from conductor.db.collections_.division import DivisionCollection
from conductor.db.collections_.mailcode import EmailCodeCollection
from conductor.db.collections_.roadmap import RoadmapCollection
from conductor.db.collections_.user import UserCollection


class DB:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.database = self.client.get_database(db_name)

        self.user = UserCollection(self.database.get_collection('user'))
        self.roadmap = RoadmapCollection(self.database.get_collection('roadmap'))
        self.mail_code = EmailCodeCollection(self.database.get_collection('email_code'))
        self.division = DivisionCollection(self.database.get_collection('division'))

        self.collections = [
            self.user,
            self.roadmap,
            self.mail_code,
            self.division
        ]

    def drop(self):
        for col in self.collections:
            col.pymongo_collection.drop()
