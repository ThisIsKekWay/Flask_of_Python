# Необходимо создать базу данных для интернет-магазина.
# База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
#
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
#
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
#
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
#
# • Таблица пользователей должна содержать следующие поля:
#         id (PRIMARY KEY),
#         имя,
#         фамилия,
#         адрес электронной почты,
#         пароль.
# • Таблица заказов должна содержать следующие поля:
#         id (PRIMARY KEY),
#         id пользователя (FOREIGN KEY),
#         id товара (FOREIGN KEY),
#         дата заказа
#         статус заказа.
# • Таблица товаров должна содержать следующие поля:
#         id (PRIMARY KEY),
#         название,
#         описание,
#         цена.

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from HW6.routers import users, products, orders
from HW6.dbmodels import database


app = FastAPI()
templates = Jinja2Templates(directory='./HW6/templates')
app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(orders.router, tags=["orders"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})
