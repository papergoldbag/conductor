import pymongo

from conductor.db.collections_.base import BaseCollection


class UserCollection(BaseCollection):
    def ensure_indexes(self):
        super().ensure_indexes()
        self.pymongo_collection.create_index(
            [("email", pymongo.ASCENDING)],
            unique=True
        )
