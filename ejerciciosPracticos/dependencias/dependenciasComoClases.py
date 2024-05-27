from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

dumbs_items_db = [{"item_name": "One"}, {"item_name": "Two"}, {"item_name": "Three"}]

class CommonQueryParameters:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParameters, Depends(CommonQueryParameters)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = dumbs_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response