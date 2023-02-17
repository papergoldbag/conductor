from __future__ import annotations

import logging
from datetime import datetime
from ipaddress import IPv4Address, IPv4Interface
from typing import Union, Any, Optional, TypeVar

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor, AsyncIOMotorDatabase
from pydantic import BaseModel, Extra, Field
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, DeleteResult

log = logging.getLogger('base_collection')

Document = dict[str, Any]
Filter = dict[str, Any]
WhatToReturn = Optional[Union[dict[str, bool], list[str]]]
Sort = list[tuple[str, int]]
Id = Union[int, str, ObjectId]


class BaseFields:
    oid = '_id'
    int_id = 'int_id'
    created = 'created'

    @classmethod
    def set(cls) -> set[str]:
        keys = list(BaseFields.__dict__.values()) + list(cls.__dict__.values())
        return {
            v
            for v in keys
            if isinstance(v, str) and not v.startswith('__') and not v.endswith('__') and v != 'set'
        }


class NotSet:
    pass


class BaseCollection:
    COLLECTION_NAME = 'base'

    def __init__(self, collection: AsyncIOMotorCollection):
        self.__collection = collection

    @classmethod
    def from_mongo_db(cls, mongo_db: AsyncIOMotorDatabase) -> BaseCollection:
        return cls(mongo_db.get_collection(cls.COLLECTION_NAME))

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.__collection

    """ENSURE ALL INDEXES"""

    async def ensure_indexes(self):
        await self.__collection.create_index([(BaseFields.int_id, pymongo.ASCENDING)], unique=True, sparse=True)
        log.info(f'base indexes were ensured on "{self.collection.name}"')

    """UTILS"""

    def __clear_from_unset(self, data: Optional[dict]) -> Document:
        res = {}
        for k, v in data.items():
            if v is NotSet:
                continue
            res[k] = v
        return res

    def __normalize_what_to_return(self, what_to_return: WhatToReturn) -> WhatToReturn:
        if isinstance(what_to_return, list):
            return {k: True for k in what_to_return}
        elif isinstance(what_to_return, dict) or what_to_return is None:
            return what_to_return
        else:
            raise TypeError(f'{type(what_to_return)} is not supported')

    def create_cursor(
            self,
            *,
            filter_: Filter = None,
            what_to_return: WhatToReturn = None,
            limit: int = None,
            skip: int = None,
            sort_: Sort = None
    ) -> AsyncIOMotorCursor:
        if filter_ is None:
            filter_ = {}
        filter_ = self.__clear_from_unset(filter_)
        what_to_return = self.__normalize_what_to_return(what_to_return)
        cursor: Cursor = self.__collection.find(filter_, what_to_return)
        if limit is not None:
            cursor = cursor.limit(limit)
        if skip is not None:
            cursor = cursor.skip(skip)
        if sort_ is not None:
            cursor = cursor.sort(sort_)
        return cursor

    def create_id_filter(
            self,
            id_: Union[Id, NotSet],
            key_oid: str = BaseFields.oid,
            key_int_id: str = BaseFields.int_id
    ) -> Filter:
        if id_ is NotSet:
            return {}
        filter_ = {}
        if isinstance(id_, int):
            filter_[key_int_id] = id_
        elif isinstance(id_, ObjectId):
            filter_[key_oid] = id_
        elif isinstance(id_, str):
            filter_[key_oid] = ObjectId(id_)
        else:
            raise ValueError('id_ is int or ObjectId')
        return filter_

    """INSERT"""

    async def generate_int_id(self) -> int:
        cursor = self.create_cursor(
            filter_={},
            what_to_return={BaseFields.int_id: True, BaseFields.oid: False},
            sort_=[(BaseFields.int_id, pymongo.DESCENDING)],
            limit=1
        )
        last_doc = None
        async for doc in cursor:
            last_doc = doc
            break
        return last_doc[BaseFields.int_id] + 1 if last_doc is not None else 1

    async def insert_document(self, document: Document) -> Document:
        if document.get(BaseFields.int_id) is None:
            document[BaseFields.int_id] = await self.generate_int_id()
        if document.get(BaseFields.created) is None:
            document[BaseFields.created] = datetime.utcnow()
        if BaseFields.oid in document and not isinstance(document[BaseFields.oid], ObjectId):
            del document[BaseFields.oid]
        inserted: InsertOneResult = await self.__collection.insert_one(document)
        document[BaseFields.oid] = inserted.inserted_id
        return document

    """GET"""

    async def get_document(
            self, filter_: Optional[Filter] = None, what_to_return: WhatToReturn = None
    ) -> Optional[Document]:
        filter_ = self.__clear_from_unset(filter_)
        what_to_return = self.__normalize_what_to_return(what_to_return)
        document = await self.__collection.find_one(filter_, what_to_return)
        return document

    async def get_document_by_id(
            self, id_: Id, what_to_return: WhatToReturn = None
    ) -> Optional[Document]:
        filter_ = self.create_id_filter(id_)
        return await self.get_document(filter_, what_to_return)

    async def get_document_by_oid(
            self, oid: ObjectId, what_to_return: WhatToReturn = None
    ) -> Optional[Document]:
        return await self.get_document({BaseFields.oid: oid}, what_to_return)

    async def get_document_by_int_id(
            self, int_id: int, what_to_return: WhatToReturn = None
    ) -> Optional[Document]:
        return await self.get_document({BaseFields.int_id: int_id}, what_to_return)

    async def get_documents(self, cursor: AsyncIOMotorCursor) -> list[Document]:
        return [doc async for doc in cursor]

    """ADDS"""

    async def count_documents(self, filter_: Optional[Filter] = None) -> int:
        filter_ = self.__clear_from_unset(filter_)
        return await self.__collection.count_documents(filter_)

    async def document_exists(self, filter_: Optional[Filter] = None) -> bool:
        return await self.count_documents(filter_) > 0

    async def id_exists(self, id_: Id) -> bool:
        return await self.document_exists(self.create_id_filter(id_))

    async def int_id_exists(self, int_id: Optional[int]) -> bool:
        return await self.document_exists({BaseFields.int_id: int_id})

    async def oid_exists(self, oid: Optional[ObjectId]) -> bool:
        return await self.document_exists({BaseFields.oid: oid})

    """UPDATE"""

    async def update_document(self, filter_: Filter, set_: Document):
        set_ = self.__clear_from_unset(set_)
        filter_ = self.__clear_from_unset(filter_)
        await self.__collection.update_one(filter_, {'$set': set_})

    async def update_document_by_id(self, id_: Id, update: Document):
        await self.update_document(self.create_id_filter(id_), update)

    """REMOVE"""

    async def remove_document(self, filter_: Filter):
        filter_ = self.__clear_from_unset(filter_)
        res: DeleteResult = await self.__collection.delete_one(filter_)

    async def remove_by_id(self, id_: Id):
        await self.remove_document(self.create_id_filter(id_))

    async def remove_by_oid(self, oid: ObjectId):
        await self.remove_document({BaseFields.oid: oid})

    async def remove_by_int_id(self, int_id: int):
        await self.remove_document({BaseFields.int_id: int_id})

    async def remove_documents(self, filter_: Filter):
        filter_ = self.__clear_from_unset(filter_)
        res: DeleteResult = await self.__collection.delete_many(filter_)

    async def drop_collection(self):
        await self.__collection.drop()
        log.info(f'collection "{self.__collection.name}" was removed')


class BaseDBM(BaseModel):
    oid: Optional[ObjectId] = Field(alias=BaseFields.oid)
    int_id: Optional[int] = Field(alias=BaseFields.int_id)
    created: Optional[datetime] = Field(alias=BaseFields.created)

    class Config:
        extra = Extra.forbid
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @classmethod
    def parse_document(cls, doc: Document) -> BaseDBM:
        return cls.parse_obj(doc)

    def document(self) -> Document:
        doc = self.dict(by_alias=True, exclude_none=False, exclude_unset=False, exclude_defaults=False)
        for f in self.__fields__.values():
            if f.alias not in doc:
                continue
            if doc[f.alias] is None:
                continue
            elif f.outer_type_ in [IPv4Interface, IPv4Address]:
                doc[f.alias] = str(doc[f.alias])
            elif f.outer_type_ in [list[IPv4Interface], list[IPv4Address]]:
                doc[f.alias] = [str(ip) for ip in doc[f.alias]]
        return doc


base = BaseDBM()

BaseDBMType = TypeVar('BaseDBMType', bound=BaseDBM)


class BaseCollectionDBM(BaseCollection):
    DBM = BaseDBM

    def __init__(self, collection: AsyncIOMotorCollection, dbm_type: type[BaseDBM]):
        super().__init__(collection)
        self.dbm_type = dbm_type

    @classmethod
    def from_mongo_db(cls, mongo_db: AsyncIOMotorDatabase) -> BaseCollectionDBM:
        return cls(mongo_db.get_collection(cls.COLLECTION_NAME), cls.DBM)

    """INSERT"""

    async def insert_dbm(self, dbm: BaseDBM) -> BaseDBMType:
        doc = await self.insert_document(dbm.document())
        dbm.oid = doc[BaseFields.oid]
        dbm.int_id = doc[BaseFields.int_id]
        dbm.created = doc[BaseFields.created]
        return dbm

    """GET"""

    async def get_dbm_by_id(self, id_: Id) -> Optional[BaseDBMType]:
        doc = await self.get_document_by_id(id_)
        if doc is None:
            return None
        return self.dbm_type.parse_document(doc)

    async def get_dbm_by_oid(self, oid: ObjectId) -> Optional[BaseDBMType]:
        doc = await self.get_document_by_oid(oid)
        if doc is None:
            return None
        return self.dbm_type.parse_document(doc)

    async def get_dbm_by_int_id(self, int_id: int) -> Optional[BaseDBMType]:
        doc = await self.get_document_by_int_id(int_id)
        if doc is None:
            return None
        return self.dbm_type.parse_document(doc)