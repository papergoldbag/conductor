import pymongo

from conductor.db.collections_.base import BaseCollection


class DivisionCollection(BaseCollection):
    def ensure_indexes(self):
        super().ensure_indexes()
        self.pymongo_collection.create_index(
            [("title", pymongo.ASCENDING)],
            unique=True
        )
