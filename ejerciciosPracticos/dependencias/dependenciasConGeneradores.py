from typing import Annotated
from fastapi import FastAPI, Depends,HTTPException

app = FastAPI()
data = {
    "data_one": {"description": "Description data one", "owner": "Owner 1"},
    "data_two": {"description": "Description data two", "owner": "Owner 2"}
}

class OwnerError(Exception):
    pass

def get_username():
    try:
        yield "Owner 1"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")
    
@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data: 
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item