from fastapi import APIRouter

from conductor.core.misc import db
from conductor.db.models import ProductDBM

shop_router = APIRouter()


@shop_router.get("", response_model=list[ProductDBM])
async def get_all_products():
    product_docs = db.product.get_all_docs()
    return product_docs
