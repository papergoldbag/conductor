from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, Body
from starlette import status

from conductor.api.dependencies import make_strict_depends_on_roles, get_current_user
from conductor.api.schemas.shop import ShopItem
from conductor.api.schemas.mailcode import OperationStatus
from conductor.core.misc import db
from conductor.db.models import UserDBM, ShopDBM, Roles

shop_router = APIRouter()


@shop_router.post("", response_model=ShopDBM)
async def create_item(
        user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor])),
        item_to_create: ShopItem = Body()
):
    item = ShopDBM(**item_to_create.dict())
    
    inserted = UserDBM.parse_document(db.shop.insert_document(item.document()))

    return inserted


@shop_router.get("", response_model=list[ShopDBM])
async def get_all_items():
    items = db.shop.get_all_docs()
    return items


@shop_router.get(".by_int_id", response_model=ShopDBM)
async def get_item_by_int_id(
    int_id: int
):
    item = db.shop.get_document_by_int_id(int_id)
    if item is None:
        return None
    item = ShopDBM.parse_document(item)
    return item


@shop_router.get('.by_item_by_int_id', response_model=OperationStatus)
async def by_item_by_int_id(
    item_int_id: int,
    current_user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor]))
):
    item = db.shop.get_document_by_int_id(item_int_id)
    if item is None:
        return OperationStatus(is_done=False)
    item: ShopDBM = ShopDBM.parse_document(item)
    if current_user.coins < item.cost:
        return OperationStatus(is_done=False)
    current_user.byed_items.append(item_int_id)
    current_user.coins = current_user.coins - item.cost

    db.user.update_document_by_int_id(current_user.int_id, current_user.document())

    return OperationStatus(is_done=True)

