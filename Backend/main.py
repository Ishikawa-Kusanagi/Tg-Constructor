from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests

# === Настройки Telegram ===



def notify_admin(order):
    text = f"Новый заказ!\nID: {order['id']}\nИмя: {order['customer_name']}\nТелефон: {order['customer_phone']}\nАдрес: {order['customer_address']}\nТовары:\n"
    for item in order["items"]:
        text += f"- Товар ID: {item['product_id']} x {item['quantity']}\n"
    # Отправляем сообщение в Telegram
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
    )


# === Модели данных ===
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str = ""
    image_url: str = ""


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class Order(BaseModel):
    id: int
    items: List[OrderItem]
    customer_name: str
    customer_phone: str
    customer_address: str


# === Данные (для MVP) ===
products = [
    Product(id=1, name="Суши сет", price=500, description="Вкусно!"),
    Product(
        id=2, name="Ролл Филадельфия", price=250, description="Свежий сыр и лосось"
    ),
    Product(id=3, name="Ролл Калифорния", price=300, description="Сыр, авокадо, краб"),
]

orders: List[Order] = []

# === Инициализация FastAPI ===
app = FastAPI(title="Mini App MVP")

# Разрешаем все источники для локальной разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Эндпоинты ===
@app.get("/products", response_model=List[Product])
def get_products():
    return products


@app.post("/orders")
def create_order(order: Order):
    orders.append(order)
    notify_admin(order.dict())  # уведомление в Telegram
    return {"status": "ok", "order_id": order.id}


@app.get("/orders", response_model=List[Order])
def get_orders():
    return orders
