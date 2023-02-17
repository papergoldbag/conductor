from __future__ import annotations

from datetime import datetime
from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel, Field, Extra

Document = dict[str, Any]


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


class BaseInDB(BaseModel):
    oid: Optional[ObjectId] = Field(alias=BaseFields.oid)
    int_id: Optional[int] = Field(alias=BaseFields.int_id)
    created: Optional[datetime] = Field(alias=BaseFields.created)

    class Config:
        extra = Extra.forbid
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @classmethod
    def parse_document(cls, doc: Document) -> BaseInDB:
        return cls.parse_obj(doc)

    def document(self) -> Document:
        return self.dict(by_alias=True, exclude_none=False, exclude_unset=False, exclude_defaults=False)
