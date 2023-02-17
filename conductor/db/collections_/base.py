from datetime import datetime

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from conductor.db.base import BaseFields, Document


class BaseCollection:
    def __init__(self, pymongo_collection: Collection):
        self.pymongo_collection = pymongo_collection

    def generate_int_id(self) -> int:
        docs = list(self.pymongo_collection.find())
        if not docs:
            return 0
        docs.sort(key=lambda d: d[BaseFields.int_id], reverse=True)
        return docs[0][BaseFields.int_id] + 1

    def insert_document(self, document: Document) -> Document:
        if document.get(BaseFields.int_id) is None:
            document[BaseFields.int_id] = self.generate_int_id()
        if document.get(BaseFields.created) is None:
            document[BaseFields.created] = datetime.utcnow()
        if BaseFields.oid in document and not isinstance(document[BaseFields.oid], ObjectId):
            del document[BaseFields.oid]
        inserted: InsertOneResult = self.pymongo_collection.insert_one(document)
        document[BaseFields.oid] = inserted.inserted_id
        return document
