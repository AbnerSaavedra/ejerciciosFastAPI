from fastapi import FastAPI
from validacionesPydantic import User
 
app = FastAPI()

dumb_items = [{"item_name": "One"}, {"item_name": "Two"}, {"item_name": "Three"}]

@app.get('/')
def home():
    return {"message": "Hello World"}

@app.get('/items/{item_id}')
async def read_item(item_id):
    return {'item_id': item_id}

@app.get('/itemInt/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}

@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 0):
    return [{skip: skip + limit}]

@app.get('/greet/{name}')
def greet(name: str) -> str:
    return f"Hello, {name}"





