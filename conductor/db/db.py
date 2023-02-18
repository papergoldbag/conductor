import logging

from pymongo import MongoClient

from conductor.db.collections_.division import DivisionCollection
from conductor.db.collections_.event import EventCollection
from conductor.db.collections_.mailcode import EmailCodeCollection
from conductor.db.collections_.roadmap import RoadmapCollection
from conductor.db.collections_.roadmap_template import RoadmapTemplateCollection
from conductor.db.collections_.user import UserCollection

log = logging.getLogger(__name__)


class DB:
    def __init__(self, mongo_uri: str, db_name: str):
        self.__mongo_client = MongoClient(mongo_uri)
        self.__mongo_database = self.__mongo_client.get_database(db_name)

        self.user = UserCollection(self.__mongo_database.get_collection('user'))
        self.roadmap = RoadmapCollection(self.__mongo_database.get_collection('roadmap'))
        self.mail_code = EmailCodeCollection(self.__mongo_database.get_collection('email_code'))
        self.division = DivisionCollection(self.__mongo_database.get_collection('division'))
        self.roadmap_template = RoadmapTemplateCollection(self.__mongo_database.get_collection('roadmap_template'))
        self.event = EventCollection(self.__mongo_database.get_collection('event'))

        self.collections = [
            self.user,
            self.roadmap,
            self.mail_code,
            self.division,
            self.roadmap_template,
            self.event
        ]

    def ensure_indexes(self):
        for collection in self.collections:
            collection.ensure_indexes()
        log.info('indexes were ensured')

    def drop(self):
        for col in self.collections:
            col.pymongo_collection.drop()
        for collection in self.__mongo_database.list_collections():
            self.__mongo_database.get_collection(collection.get('name')).drop()
