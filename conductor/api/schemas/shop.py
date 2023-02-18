from pydantic import BaseModel

class ShopItem(BaseModel):
    title: str
    description: str
    cost: int