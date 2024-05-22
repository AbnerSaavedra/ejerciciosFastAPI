from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Any

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

class User(BaseModel):
    username: str
    full_name: str | None = None

app = FastAPI() 

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )

@app.get("/items/", status_code=status.HTTP_201_CREATED)
async def read_items() -> Any:

    #return 10

    return [
        Item(name="Item1", price=10),
        Item(name="Item2", price=20)
    ]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

@app.get("/form")
def get_form(request: Request):
    result = "Ingrese un número."
    return templates.TemplateResponse("formItem.html", 
                                      context={'request':request, 'result': result})

@app.post("/form")
def post_form(request: Request, numero: int = Form(...)):
    result = numero
    return templates.TemplateResponse("formItem.html", 
                                      context={'request':request, 'result': result})
                                          
