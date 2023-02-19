from typing import Optional

from fastapi import APIRouter, Depends, Query

from conductor.api.dependencies import get_strict_current_user
from conductor.api.schemas.mailcode import OperationStatus
from conductor.core.misc import db
from conductor.db.models import ProductDBM, UserDBM

shop_router = APIRouter()


class InfoProductDBM(ProductDBM):
    already_bought: bool


@shop_router.get("", response_model=list[InfoProductDBM])
async def get_all_products(current_user: UserDBM = Depends(get_strict_current_user)):
    product_docs = db.product.get_all_docs()

    res = []
    for product_doc in product_docs:
        already_bought = product_doc['int_id'] in current_user.purchased_product_int_ids
        res.append(InfoProductDBM(
            already_bought=already_bought,
            **product_doc
        ))

    return res


@shop_router.get(".product_by_int_id", response_model=Optional[InfoProductDBM])
async def get_product_by_int_id(
        product_int_id: int = Query(),
        current_user: UserDBM = Depends(get_strict_current_user)
):
    product_doc = db.product.get_document_by_int_id(product_int_id)
    if product_doc is None:
        return None

    product_doc['already_bought'] = product_doc['int_id'] in current_user.purchased_product_int_ids

    return InfoProductDBM.parse_obj(product_doc)


@shop_router.get('.buy_product', response_model=OperationStatus)
async def buy_product(
        product_int_id: int,
        current_user: UserDBM = Depends(get_strict_current_user)
):
    product_doc = db.product.get_document_by_int_id(product_int_id)
    if product_doc is None:
        return OperationStatus(is_done=False)

    # already has bought
    if product_doc['int_id'] in current_user.purchased_product_int_ids:
        return OperationStatus(is_done=False)

    product_dbm:ProductDBM = ProductDBM.parse_document(product_doc)
    if current_user.coins < product_dbm.cost:
        return OperationStatus(is_done=False)
    current_user.purchased_product_int_ids.append(product_dbm.int_id)
    current_user.coins = current_user.coins - product_dbm.cost

    db.user.update_document_by_int_id(current_user.int_id, current_user.document())

    return OperationStatus(is_done=True)
