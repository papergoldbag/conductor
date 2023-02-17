from pymongo import MongoClient

from conductor.db.collections_.mailcode import EmailCodeCollection
from conductor.db.collections_.user import UserCollection
from conductor.db.collections_.roadmap import RoadmapCollection


class DB:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.database = self.client.get_database(db_name)

    @property
    def user(self) -> UserCollection:
        return UserCollection(self.database.get_collection('user'))
     
    @property
    def roadmap(self) -> RoadmapCollection:
        return RoadmapCollection(self.database.get_collection('roadmap'))

    @property
    def mail_code(self) -> EmailCodeCollection:
        return EmailCodeCollection(self.database.get_collection('email_code'))
    
    @property
    def roadmap_templates(self) -> RoadmapCollection:
        return RoadmapCollection(self.database.get_collection('roadmap_templates'))

