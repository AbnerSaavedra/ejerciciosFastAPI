from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header

app = FastAPI()


async def verifyToken(x_token: Annotated[str, Header()]):
    if x_token != "token_superseguro_FastAPI":
        raise HTTPException(status_code=400, detail="X-token header invalid")
    

async def verifyKey(x_key: Annotated[str, Header()]):
    if x_key != "key_supersegura_FastAPI":
        raise HTTPException(status_code=400, detail="X-key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verifyToken), Depends(verifyKey)])
async def read_items():
    return [{"item": "One"}, {"item": "Two"}]

