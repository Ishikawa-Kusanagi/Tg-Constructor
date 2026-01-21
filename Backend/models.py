from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    image_url: str = ""


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class Order(BaseModel):
    id: int
    items: List[OrderItem]
    customer_name: str
    customer_phone: str
    customer_addres: str


"""py -3 -m uvicorn backend.main:app --reload"""